# helloworld/urls.py
from django.conf.urls import url
from helloworld import views
from helloworld.lostark.controller import lost_views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^community/coinpann', views.coin_pann_list),
    url(r'^community/dcInside', views.dc_inside_list),
    url(r'^community/ddengle', views.ddengle_list),
    url(r'^community/ppompu', views.ppompu_list),
    url(r'^community/cointalk', views.coin_talk_list),
    url(r'^community/steemit', views.steemit_list),

    url(r'^community/lostark/inven', lost_views.inven),
    url(r'^community/lostark/naver', lost_views.naver),
    url(r'^community/lostark/dcinside', lost_views.dcinside),
    #url(r'^community/lostark/official', lost_views.o),
    url(r'^community/lostark/youtube',lost_views.youtube),

    url(r'^community/robots', views.get_robots),
]
