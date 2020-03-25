

from helloworld.lostark.crawler.invenCrawler import invenCrawler
from helloworld.lostark.crawler.dcinsideCrawler import DcinsideCrawler
from bs4 import BeautifulSoup
from django.http import JsonResponse


def inven(request):
    data = invenCrawler(request)
    card_list = data.get_cards() or []

    return JsonResponse(card_list, safe=False)


def naver(request):
    return "ll"


def dcinside(request):
    data = DcinsideCrawler(request)
    card_list = data.get_cards() or []

    return JsonResponse(card_list, safe=False)


def official(request):
    data = officialCrawler(request)
    card_list = data.get_cards() or []
    return "ll"


def youtube(request):

    return "ll"