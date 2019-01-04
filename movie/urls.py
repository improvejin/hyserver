from django.urls import path

from . import views


urlpatterns = [
    path(r'', views.get_movies, name='movies_info'),
    path(r'<int:movie_id>/price/', views.get_movie_price, name='movie_price'),
]