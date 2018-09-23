import requests
import json
import logging
from bs4 import BeautifulSoup


class SteemitCrawler:

    def __init__(self, json_data, markup='html.parser', timeout=5):
        self.__requests = requests.session()
        self.__markup = markup
        self.__timeout = timeout
        self.__json_data = json_data
        self.__page = 0
        self.__url = "https://api.steemit.com/"

    def set_init(self):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'if-none-match': 'e1a7-oXg31EPZ3oaoujgxEJjNN9WMo3s',
            'Referer': 'https://www.google.co.kr/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        }

        id = self.__json_data['id']
        jsonrpc = self.__json_data['jsonrpc']
        method = self.__json_data['method']
        params = self.__json_data['params']

        parameter = {'id': id, 'jsonrpc': jsonrpc, 'method': method, "params": params}
        url = self.__url
        packet_map = {
            'header': header,
            'parameter': parameter,
            'url': url
        }
        return packet_map

    def post(self):
        packet_map = self.set_init()
        try:
            response = self.__requests.post(packet_map['url'], data=json.dumps(packet_map['parameter']), headers=packet_map['header'])
        except requests.ConnectionError as e:
            self.logger.error("OOPS!! Connection Error. Make sure you are connected to Internet. "
                              "Technical Details given below.: %s", str(e))
        except requests.Timeout as e:
            self.logger.error("OOPS!! Timeout Error: %s", str(e))

        except requests.RequestException as e:
            self.logger.error("OOPS!! General Error: %s", str(e))

        return response.json()

    def parse_when_page_is_zero(self, raw_json):
        result = []
        steemit_main_url = "https://steemit.com"
        content_dict = raw_json.get('result').get('content')
        content_dict_keys = content_dict.keys()

        for key in content_dict_keys:
            card = content_dict[key]

            title = card.get('title')
            short_url = card.get('url')
            author = card.get('root_author')
            permlink = card.get('root_permlink')
            creadted_date = card.get('created')

            url = steemit_main_url + short_url
            temp_dict = {"community_name": 'steemit', 'title': title, 'url': url, 'author': author, 'permlink': permlink, 'created_date': creadted_date}
            result.append(temp_dict)

        return result

    def parse_page_is_not_zero(self, raw_json):
        result = []
        steemit_main_url = "https://steemit.com"
        content_dict = raw_json.get('result')

        for card in content_dict:

            title = card.get('title')
            short_url = card.get('url')
            author = card.get('root_author')
            permlink = card.get('root_permlink')
            creadted_date = card.get('created')

            url = steemit_main_url + short_url
            temp_dict = {"community_name": 'steemit', 'title': title, 'url': url, 'author': author,
                         'permlink': permlink, 'created_date': creadted_date}
            result.append(temp_dict)

        return result

