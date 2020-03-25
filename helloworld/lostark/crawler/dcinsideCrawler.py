
import requests
from bs4 import BeautifulSoup


class DcinsideCrawler:

    def __init__(self, request, page=1):
        self.session = requests.session()
        self.url = "http://gall.dcinside.com/mgallery/board/lists/?id=lostark"
        self.requests = request
        self.pages = self.requests.GET.get('page') or page

    def get_cards(self):
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
        parameter = {'id': 'lostark', 'page': self.pages}
        r = self.session.get(self.url, params=parameter, headers=header)
        return self.__parse_html(r.text)

    def __parse_html(self, raw_data):
        result = []
        main_url = "gall.dcinside.com/"
        bsObj = BeautifulSoup(raw_data, 'html.parser')
        card_list = bsObj.select('div.gall_listwrap.list > table > tbody > tr')

        for index, card in enumerate(card_list):
            if index > 3:
                title = card.find('a').text
                detail_url = card.find('a').attrs.get('href')
                url = main_url + detail_url
                created_date = card.find('td', class_="gall_date").contents[0]
                temp_dict = {"community_name": "dcinside", "title": title,
                             "url": url, "created_date": created_date}
                result.append(temp_dict)
            else:
                continue

        return result


