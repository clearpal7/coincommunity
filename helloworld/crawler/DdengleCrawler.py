import requests
from bs4 import BeautifulSoup


class DdengleCrawler:

    def __init__(self, page=1, markup='html.parser', timout=5):
        self.__requests = requests.session()
        self.__url = "https://www.ddengle.com/board_vote_all"
        self.__page = page
        self.__mark_up = markup

    def set_init(self):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
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
            temp_dict = {"community_name": "DDENGLE", "title": title, "url": url}
            result.append(temp_dict)
        return result