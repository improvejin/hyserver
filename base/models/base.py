from django.db import models


class ChannelBase:
    @classmethod
    def get_channel_name(cls):
        pass


class CityBase(models.Model):
    id = models.IntegerField(primary_key=True)
    g = models.CharField('分组', max_length=2)
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', db_column='update_time', auto_now=True)

    class Meta:
        abstract = True


class CinemaBase(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=10)
    district = models.CharField('区域', max_length=10)
    addr = models.CharField(max_length=50)
    phone = models.CharField(max_length=30, null=True)
    lat_lng = models.CharField(max_length=50)
    # location point
    # precise,confidence参考http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding
    # 1为精确查找， 0为不精确
    precise = models.SmallIntegerField()
    confidence = models.SmallIntegerField()
    min_price = models.FloatField('起售价，不断更新', default=0)
    price_update_time = models.DateTimeField('价格更新时间')
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', db_column='update_time', auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def get_db_table(cls):
        return 'cinema_{}'.format(cls.get_channel_name())

    def __str__(self):
        return '{}_{}_{}'.format(self.__class__.get_channel_name(), self.id, self.name)


class MatchCinemaBase(models.Model):
    """存储mt与其他渠道匹配结果"""
    id_mt = models.IntegerField(primary_key=True, verbose_name='id_mt')
    id_matched = models.IntegerField(help_text='匹配上的id')
    match_type = models.IntegerField(help_text='匹配方式 1:phone, 2:address, 4:name')
    match_score = models.FloatField(help_text='匹配score, 介于0到1之间')
    match_step = models.IntegerField(help_text='此结果是在哪一匹配step中形成')
    is_delete = models.IntegerField()
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', db_column='update_time', auto_now=True)

    def __str__(self):
        return '{}_{}'.format(self.id_mt, self.id_matched)

    class Meta:
        abstract = True


class MovieBase(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    name = models.CharField(max_length=30)
    actors = models.CharField(max_length=150)
    score = models.FloatField()
    poster = models.CharField(max_length=50)
    ongoing = models.IntegerField()
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', db_column='update_time', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class MatchMovieBase(models.Model):
    """存储db与其他渠道匹配结果"""
    id_db = models.IntegerField(primary_key=True, verbose_name='id_db')
    id_matched = models.IntegerField(help_text='匹配上的id')
    match_type = models.IntegerField(help_text='匹配方式 1:phone, 2:address, 4:name')
    match_score = models.FloatField(help_text='匹配score, 介于0到1之间')
    match_step = models.IntegerField(help_text='此结果是在哪一匹配step中形成')
    is_delete = models.IntegerField()
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', db_column='update_time', auto_now=True)

    def __str__(self):
        return '{}_{}'.format(self.id_db, self.id_matched)

    class Meta:
        abstract = True


class PriceBase(models.Model):
    """存储mt与其他渠道匹配结果"""
    # cinema_id = models.IntegerField(primary_key=True)
    show_date = models.DateField('放映日期')
    begin = models.CharField(max_length=10, help_text='开始时间')
    end = models.CharField(max_length=10, help_text='结束时间')
    language = models.CharField(max_length=10)
    hall = models.CharField(max_length=10)
    price = models.FloatField(primary_key=True)
    create_time = models.DateTimeField('create time', auto_now_add=True)
    update_time = models.DateTimeField('update time', db_column='update_time', auto_now=True)

    def __str__(self):
        return '{}_{}'.format(self.cinema_id, self.movie_id)

    class Meta:
        abstract = True
