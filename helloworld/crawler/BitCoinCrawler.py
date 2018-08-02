import requests
import logging
from bs4 import BeautifulSoup
import sys


class BitCoinCrawler:

    def __init__(self, markup='lxml', timeout=5):
        self.logger = logging.getLogger(__name__)
        self.__requests = requests.session()
        self.__markup = markup
        self.__timeout = timeout
        self.__url = "https://gall.dcinside.com/board/lists/"

    def set_init(self, gall_id, page):
        header = {
            #'Accept': 'text/html,application/xhtml_xml,application/xml;q=0.9,*/*;q=0.8',
            #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 FireFox/57.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'gall.dcinside.com',
            'Referer': 'https://www.google.co.kr/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',

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
        try:
            response = self.__requests.get(packet_map['url'], params=packet_map['parameter'], headers=packet_map['header'])
            print(sys.getsizeof(response))
        except requests.ConnectionError as e:
            self.logger.error("OOPS!! Connection Error. Make sure you are connected to Internet. "
                              "Technical Details given below.: %s", str(e))
        except requests.Timeout as e:
            self.logger.error("OOPS!! Timeout Error: %s", str(e))

        except requests.RequestException as e:
            self.logger.error("OOPS!! General Error: %s", str(e))

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

    def result_parser2(self, raw_html):
        result = []
        dcinside_main_url = "gall.dcinside.com/"
        bsObj = BeautifulSoup(raw_html, self.__markup)
        dcCardList = bsObj.select('tbody > tr > td.t_subject > a')
        index = 0
        for card in dcCardList:
            title = card.text
            shortUrl = card.get('href')
            temp_dict = {"community_name": "dcInside", "title": title,
                         "url": shortUrl}
            result.append(temp_dict)

        return result