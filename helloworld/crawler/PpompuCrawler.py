import requests
import re
import lxml
import logging
from bs4 import BeautifulSoup


class PpompuCrawler:

    def __init__(self, page, size, markup='html.parser', timeout=5):
        self.__requests = requests.session()
        self.__url = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=bitcoin'
        self.__page = page
        self.__size = size
        self.__markup = markup
        self.__timeout = timeout

    def set_init(self):
        header = {
            'Accept': 'text/html,application/xhtml_xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': None,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 FireFox/57.0'
        }
        parameter = {'page': self.__page}
        url = self.__url
        packet_map = {
            'header': header,
            'parameter': parameter,
            'url': url
        }
        return packet_map

    def get_html_text(self):
        packet = self.set_init()
        r = self.__requests.get(packet['url'], headers=packet['header'])

        return r.text

    def result_parser(self, raw_html):
        result = []
        bsObj = BeautifulSoup(raw_html, self.__markup)

        contents = bsObj.find_all("tr", {"class": re.compile("^list")})

        for i in range(3, len(contents)):
            if contents[i].find("td", {"class": "list_vspace"}):
                #첫번째(0번쨰인덱스)는 유저의 닉네임을 가리킴으로 제외
                main_content = contents[i].find_all("td", {"class": "list_vspace"})[3]
                main_content_url = main_content.find("a").attrs['href']
                main_content_title = main_content.find("font").get_text()

                temp_dict = {"community_name": "Ppompu", "title": main_content_title, "url": main_content_url}
                logging.debug("Ppompu: ", temp_dict)
                result.append(temp_dict)

        return result

