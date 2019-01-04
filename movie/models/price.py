from django.db import models

from base.models.base import PriceBase
from base.models.channel import ChannelLM, ChannelTB, ChannelMT
from cinema.models.cinema import CinemaTB, CinemaMT, CinemaLM, Cinema
from movie.models.movie import MovieTB, MovieLM, MovieMT, Movie

# 渠道电影最高价，表示渠道无此电影售价信息
MAX_PRICE = 10000


class PriceLM(PriceBase, ChannelLM):
    cinema = models.ForeignKey(CinemaLM, on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(MovieLM, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'price_lm'
        managed = False
        unique_together = ('cinema', 'movie', 'show_date', 'begin')


class PriceMT(PriceBase, ChannelMT):
    cinema = models.ForeignKey(CinemaMT, on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(MovieMT, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'price_mt'
        managed = False
        unique_together = ('cinema', 'movie', 'show_date', 'begin')


class PriceTB(PriceBase, ChannelTB):
    cinema = models.ForeignKey(CinemaTB, on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(MovieTB, to_field='id', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'price_tb'
        managed = False
        unique_together = ('cinema', 'movie', 'show_date', 'begin')


class Price(models.Model):
    cinema = models.ForeignKey(Cinema, to_field='id_mt', related_name='cinema_id', on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(Movie, to_field='id_db', related_name='movie_id', on_delete=models.DO_NOTHING)
    show_date = models.DateField('放映日期')
    begin = models.CharField(max_length=10, help_text='开始时间')
    end = models.CharField(max_length=10, help_text='结束时间')
    language = models.CharField(max_length=10)
    hall = models.CharField(max_length=10)
    price_mt = models.FloatField(primary_key=True)
    price_tb = models.FloatField()
    price_lm = models.FloatField()
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', db_column='update_time', auto_now=True)

    def price_min(self):
        return min([self.price_mt, self.price_tb, self.price_lm])

    def min_channel(self):
        price_min = self.price_min()
        if self.price_mt == price_min:
            return 'mt'
        if self.price_tb == price_min:
            return 'tb'
        if self.price_lm == price_min:
            return 'lm'

    def get_channel_prices(self):
        prices = list()
        if self.price_mt != MAX_PRICE:
            prices.append(Price.ChannelPrice('mt', self.price_mt))
        if self.price_tb != MAX_PRICE:
            prices.append(Price.ChannelPrice('tb', self.price_tb))
        if self.price_lm != MAX_PRICE:
            prices.append(Price.ChannelPrice('lm', self.price_lm))
        prices.sort()
        return prices

    def to_dict(self):
        d = dict()
        d['begin'] = self.begin
        d['end'] = self.end
        d['language'] = self.language
        d['hall'] = self.hall
        d['min_price'] = self.price_min()
        d['prices'] = [channel_price.to_dict() for channel_price in self.get_channel_prices()]
        return d

    class Meta:
        db_table = 'price'
        managed = False
        unique_together = ('cinema', 'movie', 'show_date', 'begin')

    class ChannelPrice:
        def __init__(self, channel, price):
            self.channel = channel
            self.price = price

        def __le__(self, other):
            return self.price <= other.price

        def __lt__(self, other):
            return self.price < other.price

        def to_dict(self):
            d = dict()
            d['channel'] = self.channel
            d['price'] = self.price
            return d