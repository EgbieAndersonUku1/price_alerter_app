import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Parser(object):
    """"""

    @classmethod
    def parse_url_prefix_from_url(cls, url):
        """"""
        url = urlparse(url)
        return "{}://{}".format(url.scheme, url.netloc)

    @classmethod
    def parse_price_from_url_page(cls, url, tag_name, query):
        """ """
        page_content = cls._get_page_content(url)
        return cls._parse_price_from_page_content(page_content, tag_name, query)

    @classmethod
    def _get_page_content(cls, url):
        """"""
        request = requests.get(url)
        return request.content

    @classmethod
    def _parse_price_from_page_content(cls, page, tag_name, query):
        """"""
        soup = BeautifulSoup(page, 'html.parser')
        element = soup.find(tag_name, query)
        prices = element.text.strip() if element else ''

        if prices:
            return cls._get_match(search_pattern="(\d+.\d+)", pattern_to_match=prices)

    @classmethod
    def _get_match(cls, search_pattern, pattern_to_match, search=True):
        """"""
        pattern = re.compile(search_pattern)

        if search:
            match = pattern.search(pattern_to_match)
        else:
            match = pattern.match(pattern_to_match)

        return match.group() if match else ''


