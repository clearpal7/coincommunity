import requests
import logging
import lxml
from bs4 import BeautifulSoup


class DdangleCrawler:

    def __init__(self, page, size, markup='html.parser', timout=5):
        self.__requests = requests.session()
        self.__url = "https://www.ddengle.com/board_vote_all"
        self.__page = page
        self.__size = size
        self.__mark_up = markup

    def set_init(self):
        header = {
            'Accept': 'text/html,application/xhtml_xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 FireFox/57.0'
        }
        parameter = {"page": self.__page}
        url = self.__url
        packet_map = {
            'header': header,
            'parameter': parameter,
            'url': url
        }
        return packet_map

    def get_html_text(self):
        packet = self.set_init()
        r = self.__requests.get(packet['url'], params=packet['parameter'], headers=packet['header'])
        return r.text

    def result_parser(self, raw_html):
        result = []
        bsObj = BeautifulSoup(raw_html, self.__mark_up)
        ddangleList = bsObj.select('div.bd_lst_wrp > table > tbody > tr > td.title > a.hx.bubble.no_bubble')

        for card in ddangleList:
            title = card.text
            url = card.get('href')
            temp_dict = {"community_name":"DDANGLE", "title": title, "url":url}
            result.append(temp_dict)
        return result