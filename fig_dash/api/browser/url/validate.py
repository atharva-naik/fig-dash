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