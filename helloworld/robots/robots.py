import urllib.robotparser as robotparser
from ebdjango import settings


DC_INSIDE = settings.CRAWLING_URL.get("DC_INSIDE")
PPOMPU = settings.CRAWLING_URL.get("PPOMPU")
DDANGLE = settings.CRAWLING_URL.get("DDANGLE")
COINPANN = settings.CRAWLING_URL.get("COINPANN")


def isPossibleThisWebCrawling(url):
    rp = robotparser.RobotFileParser()
    rp.set_url(DC_INSIDE)
    rp.read()
    user_agent = 'GoodCrawler'
    return rp.can_fetch(user_agent, DC_INSIDE)