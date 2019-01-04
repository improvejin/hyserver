from django.db import models

from base.models.base import CityBase
from base.models.channel import ChannelTB, ChannelMT, ChannelLM


class CityLM(CityBase, ChannelLM):

    class Meta:
        db_table = 'city_lm'
        managed = False


class CityMT(CityBase, ChannelMT):

    class Meta:
        db_table = 'city_mt'
        managed = False


class CityTB(CityBase, ChannelTB):

    class Meta:
        db_table = 'city_tb'
        managed = False


class City(models.Model):
    id_mt = models.IntegerField(primary_key=True)
    id_tb = models.IntegerField()
    id_lm = models.IntegerField()
    g = models.CharField('分组', max_length=2)
    name = models.CharField(max_length=20)
    fly = models.IntegerField()
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', db_column='update_time', auto_now=True)

    class Meta:
        db_table = 'city'
        managed = False