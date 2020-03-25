
import requests
from bs4 import BeautifulSoup


class invenCrawler:

    def __init__(self, request, page=1, sort="PID"):
        self.session = requests.session()
        self.url = "http://www.inven.co.kr/board/lostark/4811"
        self.sort = sort
        self.requests = request
        self.pages = self.requests.GET.get('page') or page

    def get_cards(self):
        self.url = self.url + '?' + 'sort=' + self.sort + '&' + 'p=' + str(self.pages)
        header = {
            'Host': 'www.inven.co.kr',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/69.0.3497.100',
            'Referer': 'http://www.inven.co.kr/board/lostark/4811/49415?p=3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': 'MOBILE_V3=NONE; _ga=GA1.3.523518917.1533643341; dable_uid=77276589.1503212548089; VISIT_SITE=lostark%7Clol%7Cesports; '
                      'inven_link=stream; _gid=GA1.3.1489609002.1540572446; invenrchk=%7B%224811%7C49496%22%3A%7B%22d%22%3A%222018-10-27+01%3A52%3A38%22%2C%22s%22%3Anull%7D%2C%224811%7C49421%22%3A%7B%22d%22%3A%222018-10-27+02%3A21%3A54%22%2C%22s%22%3Anull%7D%2C%224811%7C49415%22%3A%7B%22d%22%3A%222018-10-27+02%3A22%3A01%22%2C%22s%22%3Anull%7D%7D',

        }
        parameter = {'sort': self.sort, 'p': self.pages}

        r = self.session.get(self.url, params=parameter, headers=header)
        return self.__parse_html(r.text)

    def __parse_html(self, raw_data):
        result = {}
        subjects = []
        nicks = []
        dates= []

        bsObj = BeautifulSoup(raw_data, 'html.parser')
        inven_list = bsObj.select('#powerbbsBody > table > tr > td > div > table > tr > td > table > tr:nth-of-type(3) > td > form > table > tbody > tr')

        for index, card in enumerate(inven_list):
            if index > 3:
                if card.find('td', class_='bbsSubject'):
                    subject = card.find('td', class_='bbsSubject').text
                    subjects.append(subject)
                if card.find('td', class_='bbsNick'):
                    nick = card.find('td', class_='bbsNick').text
                    nicks.append(nick)
                if card.find('td', class_='date'):
                    date = card.find('td', class_='date').text
                    dates.append(date)

            else:
                continue
        result['subject'] = subjects
        result['nick'] = nicks
        result['date'] = dates
        return result



