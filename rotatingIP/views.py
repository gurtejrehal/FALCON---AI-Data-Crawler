from django.shortcuts import HttpResponse
from rotatingIP.models import IPLink, IP
from rotatingIP.tasks import get_proxies

def index(request):
    """
    :param request:
    :return: proxies
    """
    ip_links = IPLink.objects.all()

    for link in ip_links:
        proxies = get_proxies(link)
        for proxy in proxies:
            ip = IP.objects.get_or_create(ip=proxy)[0]
            ip.save()

    return HttpResponse("success")



