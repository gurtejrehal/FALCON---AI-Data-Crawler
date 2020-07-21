from crawler import views
from django.urls import path

app_name = 'crawler'

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('test/', views.test, name='test'),
]