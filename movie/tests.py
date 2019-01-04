from django.test import TestCase

# Create your tests here.
from movie.service import MovieService


class ServiceTests(TestCase):

    service = MovieService()

    def test_get_movies_by_cinema(self):
        movies = self.service.get_movies_by_cinema(6)
        print(movies)
