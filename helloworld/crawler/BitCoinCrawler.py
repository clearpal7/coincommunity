import requests
import logging
from bs4 import BeautifulSoup
import sys


class BitCoinCrawler:

    def __init__(self, page=1, markup='html.parser', timeout=5):
        self.logger = logging.getLogger(__name__)
        self.__requests = requests.session()
        self.__markup = markup
        self.__page = page
        self.__timeout = timeout
        self.__url = "https://gall.dcinside.com/board/lists/"

    def set_init(self, gall_id, page):
        header = {
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
        parameter = {'id': gall_id, 'page': self.__page}
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

    def result_parser(self, raw_html):
        result = []
        dcinside_main_url = "gall.dcinside.com/"
        bsObj = BeautifulSoup(raw_html, self.__markup)
        dcCardList = bsObj.select('div.gall_listwrap.list > table > tbody > tr')

        index = 0
        for card in dcCardList:
            if index < 3:
                index += 1
                continue

            title = card.find('a').text
            short_url = card.find('a').attrs.get('href')
            created_date = card.find('td', class_="gall_date").contents[0]
            url = dcinside_main_url + short_url
            temp_dict = {"community_name": "dcInside", "title": title,
                         "url": url, "created_date": created_date}
            result.append(temp_dict)

        return result