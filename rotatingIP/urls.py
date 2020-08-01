from rotatingIP import views
from django.urls import path

app_name = 'rotatingIP'

urlpatterns = [
    path('', views.index, name='index'),
]