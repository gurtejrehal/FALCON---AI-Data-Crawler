from scheduler import views
from django.urls import path

app_name = 'scheduler'

urlpatterns = [
    path('', views.index, name='index'),
    path('search-link/', views.search, name='search')

]