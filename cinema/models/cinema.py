
from django.db import models

from base.models.base import CinemaBase
from base.models.channel import ChannelMT, ChannelTB, ChannelLM


class CinemaLM(CinemaBase, ChannelLM):

    class Meta:
        db_table = 'cinema_lm'
        managed = False


class CinemaMT(CinemaBase, ChannelMT):

    class Meta:
        db_table = 'cinema_mt'
        managed = False


class CinemaTB(CinemaBase, ChannelTB):

    class Meta:
        db_table = 'cinema_tb'
        managed = False


class Cinema(models.Model):
    id_mt = models.IntegerField(primary_key=True, db_column='id_mt')
    id_tb = models.IntegerField()
    id_lm = models.IntegerField()
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=10)
    district = models.CharField('区域', max_length=10)
    addr = models.CharField(max_length=50)
    lat_lng = models.CharField(max_length=50)
    min_price = models.FloatField('起售价，不断更新', default=0)
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', db_column='update_time', auto_now=True)

    class Meta:
        managed = False
        db_table = 'cinema'

    def to_dict(self):
        d = dict()
        d['id'] = self.id_mt
        d['name'] = self.name
        d['addr'] = self.addr
        d['lat_lng'] = self.lat_lng
        d['price'] = self.min_price
        return d

# class CinemaMatchResult(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='id', auto_created=True)
#     # name, addr, phone
#     # id_mt = models.IntegerField()
#     # id_tb = models.IntegerField()
#     cinema_mt = models.ForeignKey(CinemaMT, db_column='id_mt', on_delete=models.DO_NOTHING, to_field='id')
#     cinema_tb = models.ForeignKey (CinemaTB, db_column='id_tb', on_delete=models.DO_NOTHING, to_field='id')
#     cinema_lm = models.ForeignKey (CinemaLM, db_column='id_lm', on_delete=models.DO_NOTHING, to_field='id')
#
#     class Meta:
#         db_table = 'cinema_match_result'
#
#     # objects’ representations are used in django admin
#     def __str__(self):
#         return '{}_{}'.format(self.id, self.cinema_mt)