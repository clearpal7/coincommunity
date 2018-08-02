import re
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from bs4 import BeautifulSoup
from helloworld.crawler.CoinPannCrawler import CoinPannCrawler
from helloworld.crawler.BitCoinCrawler import BitCoinCrawler
from helloworld.crawler.DdangleCrawler import DdangleCrawler
from helloworld.crawler.PpompuCrawler import PpompuCrawler
import logging

from helloworld.robots import robots


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

    
def coin_pann_list(request):
    type = "coinpann"
    page = set_page_is_one(request)

    crawler = CoinPannCrawler()
    raw_html = crawler.get_html_text()

    bsobj = BeautifulSoup(raw_html, 'lxml')
    content = bsobj.find_all("td", {"class": "title"})
    result = []
    for i in range(0, len(content)):
        title = content[i].get_text()
        url = content[i].find("a")
        if url.attrs["href"] is not None:
            url = url.attrs["href"]
        temp_dict = {"community_name": type, "title": title, "url": url}
        result.append(temp_dict)

    logging.INFO(str(result))
    return JsonResponse(result, safe=False)


def dc_inside_list(request):
    gall_id = "bitcoins"
    page = set_page_is_one(request)

    crawler = BitCoinCrawler()
    raw_html = crawler.post(gall_id, page)
    result = crawler.result_parser(raw_html)

    return JsonResponse(result, safe=False)


def ddangle_list(request):
    page = set_page_is_one(request)

    crawler = DdangleCrawler(page, 10)
    raw_html = crawler.get_html_text()
    result = crawler.result_parser(raw_html)

    return JsonResponse(result, safe=False)


def ppompu_list(request):
    page = set_page_is_one(request)
    crawler = PpompuCrawler(page, 10)

    raw_html = crawler.get_html_text()
    result = crawler.result_parser(raw_html)

    return JsonResponse(result, safe=False)


def coinone_list(request):
    #코인원은 직접 클라이언트 측에서 API 호출(크롤링 필요없음)
    pass


def set_page_is_one(request):
    page = request.GET.get('page')
    if page is None:
        page = 1
    return page


def get_robots(request):
    return JsonResponse(robots.isPossibleThisWebCrawling('temp'))




