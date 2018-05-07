import requests
import re
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from bs4 import BeautifulSoup
from helloworld.crawler.CoinPannCrawler import CoinPannCrawler
from helloworld.crawler.BitCoinCrawler import BitCoinCrawler

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

    
def coin_pann_list(request):
    type = "coinpann"
    page = request.GET.get('page')
    if page is None:
      page = 1

    raw_html = CoinPannCrawler.get_html_text()

    bsobj = BeautifulSoup(raw_html, 'lxml')
    parsing_tr = bsobj.find_all("tr", {"class": re.compile("^bg")})
    content = bsobj.find_all("td", {"class": "title"})
    result = []
    for i in range(0, len(content)):
        title = content[i].get_text()
        url = content[i].find("a")
        if url.attrs["href"] is not None:
            url = url.attrs["href"]
        temp_dict = {"type": type, "title": title, "url": url}
        result.append(temp_dict)

    return JsonResponse(result, safe=False)


def dc_inside_list(request):
    gall_id = "bitcoins"
    page = request.GET.get('page')
    if page is None:
        page = 1

    crawler = BitCoinCrawler()
    raw_html = crawler.post(gall_id, page)
    result = crawler.result_parser(raw_html)

    return JsonResponse(result, safe=False)





