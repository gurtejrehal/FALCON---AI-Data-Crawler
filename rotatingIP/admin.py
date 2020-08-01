from django.contrib import admin
from rotatingIP.models import IPLink, IP

admin.site.register(IPLink)
admin.site.register(IP)