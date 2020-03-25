import os
import sys
from bs4 import BeautifulSoup
import urllib3
from datetime import datetime, timedelta
from traceback import format_exc
import to_es

dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(dir, '../save'))
base_url="http://news.naver.com/#"


def collecting(base_url):
    http = urllib3.PoolManager()
    data = http.request('GET', base_url)
    soup = BeautifulSoup(data, "html.parser")
    total_data = soup.find_all(attrs={'class': 'main_component droppable'})

    collect_time = str(datetime.utcnow().replace(microsecond=0) + timedelta(hours=9))[:16]

    for each_data in total_data:
        category = ""

        try:
            category = str(each_data.find_all(attrs={'class': 'tit_sec'})).split('>')[2][:-3]
        except:
            pass

        data = str(each_data.find_all(attrs={'class': 'mlist2 no_bg'}))

        news_list = data.split('<li>')

        for each_news in news_list[1:]:

            news_block = each_news.split('href="')[1]
            print(news_block)

            title = news_block.split('<strong>')[1].split('</strong>')[0]
            # print(title)

            news_url = news_block.split('"')[0].replace("amp;", "")
            # print(news_url)

            soup2 = BeautifulSoup(http.request('GET', news_url), "html.parser")
            # print(soup2)

            article_body = str(soup2.find_all(attrs={'id': 'articleBodyContents'}))
            insert_data = {
                "source": "naver_news",
                "category": category,
                "title": title,
                "article_body": article_body,
                "collect_time": collect_time
            }
            to_es.to_elastic(insert_data)

            
collecting(base_url)