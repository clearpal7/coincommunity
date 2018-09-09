
import requests


class CoinPannCrawler:

    def __init__(self, page=1):
        self.__requests = requests.session()
        self.__page = page
        self.__url = "https://coinpan.com/index.php"

    def get_html_text(self):
        url = self.__url
        payload = {'mid': 'free', 'page': self.__page}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'referer': 'https://coinpan.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/67.0.3396.99 Safari / 537.36'
        }
        r = self.__requests.get(url, params=payload, headers=headers)
        return r.text
