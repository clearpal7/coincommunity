 # helloworld/views.py
import requests
import re
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from bs4 import BeautifulSoup

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)
    
    
def coin_pann_list(request):
    page = request.GET.get('page')
    if page is None:
      page = 1
    raw_html = get_html_text()

    bsobj = BeautifulSoup(raw_html, 'lxml')
    parsing_tr = bsobj.find_all("tr", {"class": re.compile("^bg")})
    content = bsobj.find_all("td", {"class": "title"})
    result = []
    for i in range(0, len(content)):
        title = content[i].get_text()
        url = content[i].find("a")
        if url.attrs["href"] is not None:
            url = url.attrs["href"]
        temp_dict = {"title": title, "url": url}
        result.append(temp_dict)

    return JsonResponse(result, safe=False)


def get_html_text():
    url = "http://coinpan.com/free"
    payload = {'mid': 'free', 'page': '1'}
    headers = {
        'Accept': 'text/html,application/xhtml_xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 FireFox/57.0'
    }
    r = requests.get(url, params=payload, headers=headers)
    return r.text