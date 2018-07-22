
import requests


class CoinPannCrawler:

    def __init__(self):
        self.__requests = requests.session()
        self.__url = "http://coinpan.com/free"

    def get_html_text(self):
        url = self.__url
        payload = {'mid': 'free', 'page': '1'}
        headers = {
            'Accept': 'text/html,application/xhtml_xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 FireFox/57.0'
        }
        r = self.__requests.get(url, params=payload, headers=headers)
        return r.text
