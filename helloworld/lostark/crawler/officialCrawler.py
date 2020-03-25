import requests
from bs4 import BeautifulSoup

class officialCrawler:

    def __init__(self, request, page=1):
        self.session = requests.session()
        self.url = "https://lostark.game.onstove.com/Library/Tip/List"
        self.sort = ""
        self.requests = request
        self.pages = self.requests.GET.get('page') or page


        