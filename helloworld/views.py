
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from bs4 import BeautifulSoup
from helloworld.crawler.CoinPannCrawler import CoinPannCrawler
from helloworld.crawler.BitCoinCrawler import BitCoinCrawler
from helloworld.crawler.DdengleCrawler import DdengleCrawler
from helloworld.crawler.PpompuCrawler import PpompuCrawler
from helloworld.crawler.CoinTalkCrawler import CoinTalkCrawler
from helloworld.crawler.SteemitCrawler import SteemitCrawler
from django.views.decorators.csrf import csrf_exempt

from helloworld.robots import robots
import json


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


def coin_pann_list(request):
    type = "coinpann"
    page = set_page_is_one(request)
    crawler = CoinPannCrawler(page)
    raw_html = crawler.get_html_text()

    bsObj = BeautifulSoup(raw_html, 'html.parser')
    coinPannList = bsObj.select('table > tbody > tr > td.title > a:nth-of-type(1)')
    coin_pann_list_time = bsObj.select('table > tbody > tr > td.time')
    result = []

    index = 5
    for coinPann in coinPannList[5:]:
        title_with_EOL = coinPann.text
        title = title_with_EOL.replace("  ", "").replace("\n","")
        url = coinPann.get('href')
        if index < coin_pann_list_time.__len__():
            created_dated = coin_pann_list_time[index].find('span', class_="regdateHour").text
            index += 1
        temp_dict = {"community_name": type, "title": title, "url": url, "created_date": created_dated}
        result.append(temp_dict)

    return JsonResponse(result, safe=False)


def dc_inside_list(request):
    gall_id = "bitcoins"
    page = set_page_is_one(request)

    crawler = BitCoinCrawler(page)
    raw_html = crawler.post(gall_id, page)
    result = crawler.result_parser(raw_html)

    return JsonResponse(result, safe=False)


def coin_talk_list(request):
    page = set_page_is_one(request)
    crawler = CoinTalkCrawler(page)
    raw_html = crawler.post()
    result = crawler.result_parser(raw_html)

    return JsonResponse(result, safe=False)


def ddengle_list(request):
    page = set_page_is_one(request)

    crawler = DdengleCrawler(page)
    raw_html = crawler.get_html_text()
    result = crawler.result_parser(raw_html)

    return JsonResponse(result, safe=False)


@csrf_exempt
def steemit_list(request):
    #API호출
    json_data = json.loads(request.body)
    id = json_data['id']

    crawler = SteemitCrawler(json_data)
    raw_json = crawler.post()

    if id == 0:
        result = crawler.parse_when_page_is_zero(raw_json)
    else:
        result = crawler.parse_page_is_not_zero(raw_json)

    print(JsonResponse(result, safe=False))
    return JsonResponse(result, safe=False)


def ppompu_list(request):
    page = set_page_is_one(request)
    div_page = 19

    crawler = PpompuCrawler(page, div_page)
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




