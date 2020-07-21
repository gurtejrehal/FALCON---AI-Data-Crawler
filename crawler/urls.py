from crawler import views
from django.urls import path

app_name = 'crawler'

urlpatterns = [
    path('', views.index, name='index'),
]