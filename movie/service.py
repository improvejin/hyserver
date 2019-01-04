from datetime import datetime

from movie.models.price import Price


class MovieService(object):

    def get_movies_by_cinema(self, cinema_id):
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        begin = now.strftime('%H:%M')
        movies = set()
        # from django.db import connection
        f = Price.objects.filter(cinema_id=cinema_id)
        prices = f.filter(show_date__gt=today) | f.filter(show_date=today, begin__gt=begin)
        # print(connection.queries)
        for price in prices:
            movies.add(price.movie)
        return movies

    def get_movie_price(self, cinema_id, movie_id):
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        begin = now.strftime('%H:%M')
        shows = dict()
        f1 = Price.objects.filter(cinema_id=cinema_id, movie_id=movie_id)
        f2 = f1.filter(show_date__gt=today) | f1.filter(show_date=today, begin__gt=begin)
        prices = f2 .order_by('show_date', 'begin')
        for price in prices:
            if price.show_date not in shows:
                shows[price.show_date] = list()
            day_schedules = shows[price.show_date]
            day_schedules.append(price)
        return shows
