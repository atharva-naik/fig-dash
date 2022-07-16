from typing import *
from PyQt5.QtCore import QUrl

# check if a given URL has a vaild top-level domain
def isValidTLD(url: Union[str, QUrl], verbose: bool=False) -> bool:
    """check if a given URL has a vaild top-level domain

    Args:
        url (Union[str, QUrl]): url string/QUrl object.

    Returns:
        bool: output indicates if the potential URL has a valid top level domain.
    """
    if isinstance(url, QUrl):
        qurl = url
        urlString = url.toString()
    else: 
        qurl = QUrl(url)
        urlString = url
    tld = qurl.topLevelDomain()
    if verbose:
        print(f"tld: {tld}")
        print(f"url: {urlString}")
    if tld == "": return False
    elif urlString.endswith(tld):
        return True
    else: return False

def repair_url(url):
    stripped_url = url.strip(":").strip("/")
    if not stripped_url.startswith("http://"):
        fixed_url = "http://"+stripped_url

    return fixed_url

def check_url(url_or_query):
    from requests.utils import quote
    from requests.models import PreparedRequest
    from requests.exceptions import MissingSchema, InvalidURL
    prepared_request = PreparedRequest()
    url_or_query = url_or_query.strip()
    try:
        prepared_request.prepare_url(url_or_query, None)
        return prepared_request.url
    except MissingSchema as e:
        fixed_url = repair_url(url_or_query)
        try: 
            prepared_request.prepare_url(fixed_url, None)
            return prepared_request.url
        except InvalidURL as e: 
            query = quote(url_or_query)
            return f"https://www.google.com/search?q={query}&oq={query}"
    except InvalidURL as e: 
        query = quote(url_or_query)
        return f"https://www.google.com/search?q={query}&oq={query}"