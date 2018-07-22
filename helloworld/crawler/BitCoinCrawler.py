import requests
import logging
from bs4 import BeautifulSoup


class BitCoinCrawler:

    def __init__(self, markup='lxml', timeout=5):
        self.__requests = requests.session()
        self.__markup = markup
        self.__timeout = timeout
        self.__url = "http://gall.dcinside.com/board/lists/"

    def set_init(self, gall_id, page):
        header = {
            'Accept': 'text/html,application/xhtml_xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 FireFox/57.0'
        }
        parameter = {'id': gall_id, 'page': page}
        url = self.__url
        packet_map = {
            'header': header,
            'parameter': parameter,
            'url': url
        }
        return packet_map

    def post(self, gall_id, page):
        packet_map = self.set_init(gall_id, page)
        response = self.__requests.get(packet_map['url'], params=packet_map['parameter'], headers=packet_map['header'])
        logging.debug("BitCoin Gallery Crawling After Post", response)
        return response.text

    def change_url_link_from_internal_to_external(self, dc_main_url, dc_internal_url):
        external_url=''
        if dc_internal_url.attrs["href"] is not None:
            internal_url = dc_internal_url.attrs["href"]
            if internal_url.startswith("/board"):
                external_url = dc_main_url + internal_url
                return external_url
            elif internal_url.startswith("gall.dcinside.com"):
                return internal_url

    def result_parser(self, raw_html):
        result = []
        dcinside_main_url = "gall.dcinside.com/"
        bsObj = BeautifulSoup(raw_html, self.__markup)
        dt1 = bsObj.find_all("tr", {"class": "tb"})

        bsObj = BeautifulSoup(str(dt1), 'lxml')
        content = bsObj.find_all("td", {"class": "t_subject"})
        for i in range(0, len(content)):
            if content[i].find_all("a", {"class": "icon_notice"}):
                pass
            else:
                content_url = content[i].find("a")
                title = content[i].get_text()
                temp_dict = {"community_name": "dcInside", "title": title, "url": self.change_url_link_from_internal_to_external(dcinside_main_url, content_url)}
                logging.debug("BitCoinGallery: ", temp_dict)
                result.append(temp_dict)
        return result


