import requests
import logging
import lxml
from bs4 import BeautifulSoup


class DdangleCrawler:

    def __init__(self, page, size, markup='lxml', timout=5):
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
        table = bsObj.find("table", {"class": "bd_lst bd_tb_lst bd_tb"})

        bsObj = BeautifulSoup(str(table), self.__mark_up)
        contents = bsObj.find_all("td", {"class": "title"})

        for i in range(0, len(contents)):
            if contents[i].find("a", {"class": "hx bubble no_bubble"}):
                content_url = contents[i].find("a").attrs['href']
                title = contents[i].get_text()
                temp_dict = {"community_name": "Ddangle", "title": title, "url": content_url}
                logging.debug("Ddangle: ", temp_dict)
                result.append(temp_dict)

        return result