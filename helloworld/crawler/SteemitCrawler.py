import requests
import logging
from bs4 import BeautifulSoup


class SteemitCrawler:

    def __init__(self, markup = 'lxml', timeout = 5):
        self.__requests = requests.session()
        self.__markup = markup
        self.__timeout = timeout
        self.__url = ""
