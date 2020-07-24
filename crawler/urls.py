from crawler import views
from django.urls import path

app_name = 'crawler'

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('crawler/', views.crawler_index, name='crawler_index'),
    path('update-notifications/', views.update_notifications, name='update_notifications'),
    path('update/', views.update, name='update'),
    path('read/', views.read, name='read'),
    path('result/', views.process, name='process'),
    path('test/', views.test, name='test'),
    path('falcon-api/<str:keyword>/', views.api, name='api')
]