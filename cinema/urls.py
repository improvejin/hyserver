from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.get_cinemas, name='cinema_list'),
    path(r'search/', views.search_cinemas, name='cinema_search'),
]