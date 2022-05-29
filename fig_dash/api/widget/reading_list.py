#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("fig_dash::api::widget::reading_list")
import re
# import httplib
import requests
from bs4 import BeautifulSoup
from string import punctuation
from urllib.error import HTTPError
# from operator import itemgetter
# from collections import Counter

# def get_word_count(url):
#     content = requests.get(url).content
#     # html of web page.
#     soup = BeautifulSoup(content, features='html.parser')
#     # get words wihtin paragraph tags.
#     p = (''.join(s.findAll(text=True))for s in soup.findAll('p'))
#     # word count dict
#     word_counts_p = Counter(
#         (
#             x.rstrip(punctuation).lower() for y in p for x in y.split()
#         )
#     )
#     # get words wihtin div tags.
#     div = (''.join(s.findAll(text=True))for s in soup.findAll('div'))
#     # word count dict
#     word_counts_p = Counter(
#         (
#             x.rstrip(punctuation).lower() for y in p for x in y.split()
#         )
#     )

#     return word_counts_p + word_counts_div

# def get_webpage(site, page):
#    conn = httplib.HTTPConnection(site)
#    conn.request("GET", page)
#    rd = conn.getresponse()
#    print(rd.status, rd.reason)

#    return rd.read()

# def get_freqct(list):
#     freqct = {}
#     for s in list:
#       if s not in freqct:
#         freqct[s]=1
#       else:
#          freqct[s]+=1
#     return freqct

# def main():
#    data = get_webpage('en.wikipedia.org',"/wiki/Python_(programming_language)")
#    data = re.sub(r'<[^>]+>','',data)
#    d = get_freqct(data.split(' '))
#    sol = sorted(d.items(), key=itemgetter(1))
#    for word, count in sol:
#       print(word, ":", count)
class WordCountExtractor:
    def __init__(self):
        from boilerpy3 import extractors
        self.extractor = extractors.ArticleExtractor()

    def content_from_file(self, file: str):
        content = self.extractor.get_content_from_file(file)
        self.content = content

    def content_from_html(self, html: str):
        content = self.extractor.get_content_from_html(html)
        self.content = content

    def content_from_url(self, url):
        '''get word count from url.'''
        try:
            content = self.extractor.get_content_from_url(url)
            self.content = content
            if self.content.strip() == '''Something went wrong. Wait a moment and try again.
Try again'''.strip():
                raise FileNotFoundError
        except (HTTPError, FileNotFoundError) as e:
            print("failed to get content from boilerpy3")
            content = requests.get(url).text
            soup = BeautifulSoup(content, features="html.parser")
            # wc = 0
            self.content = ''
            for div in soup.findAll("div"):
                # wc += len(div.text.strip().split())
                # print("\x1b[31;1m"+"#"*10+"\x1b[0m")
                # print(div.text)
                # print("\x1b[31;1m"+"#"*10+"\x1b[0m")
                self.content += " " + " ".join(div.text.strip().split())
            # print(soup.prettify())
            self.content = self.content.strip()
            # print(self.content)
        return self.content

    def __call__(self, url: str):
        content = self.content_from_url(url)
        print(content)
        return len(content.strip().split())


def test_word_count():
    wce = WordCountExtractor()
    print(wce("https://timesofindia.indiatimes.com/"))


if __name__ == "__main__":
   test_word_count()