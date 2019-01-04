from django.db import models

from base.models.base import MovieBase
from base.models.channel import ChannelMT, ChannelLM, ChannelTB, ChannelDB


class MovieLM(MovieBase, ChannelLM):
    release_date = models.CharField(max_length=20)

    class Meta:
        db_table = 'movie_lm'
        managed = False


class MovieMT(MovieBase, ChannelMT):
    release_date = models.CharField(max_length=20)
    version = models.CharField(max_length=10)

    class Meta:
        db_table = 'movie_mt'
        managed = False


class MovieTB(MovieBase, ChannelTB):

    class Meta:
        db_table = 'movie_tb'
        managed = False


class MovieDB(MovieBase, ChannelDB):
    release_date = models.CharField(max_length=20)

    class Meta:
        db_table = 'movie_db'
        managed = False


class Movie(models.Model):
    id_db = models.IntegerField(primary_key=True, db_column='id_db')
    id_mt = models.IntegerField()
    id_tb = models.IntegerField()
    id_lm = models.IntegerField()
    name = models.CharField(max_length=30)
    actors = models.CharField(max_length=150)
    type = models.CharField(max_length=50)
    score = models.FloatField()
    duration = models.CharField(max_length=20)
    release_date = models.CharField(max_length=20)
    poster = models.CharField(max_length=50)
    ongoing = models.IntegerField()
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', db_column='update_time', auto_now=True)

    class Meta:
        db_table = 'movie'
        managed = False

    def to_dict(self):
        d = dict()
        d['id'] = self.id_db
        d['actiors'] = self.actors
        d['name'] = self.name
        d['type'] = self.type
        d['score'] = self.score
        d['duration'] = self.duration
        d['poster'] = self.poster
        return d