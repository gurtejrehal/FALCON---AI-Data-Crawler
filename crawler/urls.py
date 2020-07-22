from crawler import views
from django.urls import path

app_name = 'crawler'

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('update/', views.update, name='update'),
    path('read/', views.read, name='read'),
    path('result/', views.process, name='process'),
    path('test/', views.test, name='test'),
]