
import requests
from bs4 import BeautifulSoup


class CoinTalkCrawler:

    def __init__(self, mark_up='html.parser', timeout=5, page=1):
        self.__requests = requests.session()
        self.__markup = mark_up
        self.__timeout = timeout
        self.__page = page
        self.__url = "http://cointalk.co.kr/bbs/board.php?bo_table=freeboard"

    def set_init(self):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'cointalk.co.kr',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        }
        parameter = {'page': self.__page}
        url = self.__url
        packet_map = {
            'header': header,
            'parameter': parameter,
            'url': url
        }
        return packet_map

    def post(self):
        request_map = self.set_init()
        try:
            response = self.__requests.get(request_map['url'], params=request_map['parameter'], headers=request_map['header'])
        except requests.ConnectionError as e:
            self.logger.error("OOPS!! Connection Error. Make sure you are connected to Internet. "
                              "Technical Details given below.: %s", str(e))
        return response.text

    def result_parser(self, raw_html):
        result = []
        bsObj = BeautifulSoup(raw_html, self.__markup)
        coinTalkList = bsObj.select('table > tbody > tr > td.sbj > a')

        for card in coinTalkList:
            title = card.text
            url = card.get('href')
            temp_dict = {'community_name': 'coinTalk', 'title': title, 'url': url}
            result.append(temp_dict)
        return result
