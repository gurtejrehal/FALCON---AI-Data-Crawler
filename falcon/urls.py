"""
falcon URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def redirect_login(request):
    if not request.user.is_authenticated:
        return redirect('auth_login')
    else:
        return redirect('crawler:index')


urlpatterns = [
    path('', redirect_login),
    path(r'^jet/', include('jet.urls', 'jet')),
    path(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('get-proxy/', include('rotatingIP.urls')),
    path('', include('crawler.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
