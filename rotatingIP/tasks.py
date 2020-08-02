from celery import shared_task
from rotatingIP.models import IP
import requests
from lxml.html import fromstring
import random
import csv


def get_proxies(url):
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


@shared_task
def save_proxy(ip):
    proxy = IP.objects.get_or_create(ip=ip)[0]
    proxy.save()


def random_header():
    file_name = '/static/UserAgent.csv'
    UserAgentCSV = open(file_name, 'r')
    UserAgentList = csv.reader(UserAgentCSV)
    UserAgentList = [row for row in UserAgentList]
    UserAgentList = [l[0] for l in UserAgentList]
    random.shuffle(UserAgentList)

    return {'User-Agent': random.choice(UserAgentList)}