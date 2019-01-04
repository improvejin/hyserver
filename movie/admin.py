from django.contrib import admin

from movie.models.match import MatchMovieLM2DB, MatchMovieMT2DB, MatchMovieTB2DB
from movie.models.movie import MovieTB, MovieMT, MovieLM, Movie, MovieDB
from movie.models.price import PriceTB, PriceMT, PriceLM, Price


class MovieChannelAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'actors', 'score','ongoing', 'create_time', 'update_time')
    search_fields = ['id', 'name']
    list_filter = ['ongoing', 'update_time']


class MovieScoreFilter(admin.SimpleListFilter):
    title = 'score'
    parameter_name = 'score'

    def lookups(self, request, model_admin):
        scores = (('=0', '=0'), ('<6 and >0', '<6 and >0'), ('>=6', '>=6'))
        return scores

    def queryset(self, request, queryset):
        score = self.value()
        if score is not None:
            if score == '=0':
                return queryset.filter(score__lt=1)
            elif score == '<6 and >0':
                return queryset.filter(score__lt=6, score__gte=1)
            elif score == '>=6':
                return queryset.filter(score__gte=6)


class MovieFilter(admin.SimpleListFilter):
    title = '匹配情况'
    parameter_name = 'channel'

    def lookups(self, request, model_admin):
        channels = (('mt', 'mt'), ('tb', 'tb'), ('lm', 'lm'), ('others', 'others'))
        return channels

    def queryset(self, request, queryset):
        channel = self.value()
        if channel is not None:
            if channel == 'mt':
                return queryset.filter(id_mt=0)
            elif channel == 'tb':
                return queryset.filter(id_tb=0)
            elif channel == 'lm':
                return queryset.filter(id_lm=0)
            elif channel == 'others':
                return queryset.exclude(a=True).filter(id_mt__ne=0, id_tb__ne=0, id_lm__ne=0)


class MovieAdmin(admin.ModelAdmin):
    ordering = ['id_db']
    list_display = ('id_db', 'id_mt', 'id_tb', 'id_lm', 'name', 'type', 'actors', 'score', 'duration', 'ongoing', 'update_time')
    search_fields = ['name']
    list_filter = ['ongoing', MovieScoreFilter, MovieFilter, 'update_time']


class MatchMovieAdmin(admin.ModelAdmin):
    ordering = ['id_db']
    list_display = ('id_db', 'id_matched', 'match_type', 'match_score', 'match_step', 'is_delete', 'update_time')
    list_filter = ['match_type', 'match_step', 'match_score', 'match_step', 'update_time']
    search_fields = ['id_db']


class MoviePriceAdmin(admin.ModelAdmin):
    ordering = ['cinema_id', 'movie_id', 'show_date', 'begin']
    list_display = ('cinema_id', 'movie_id', 'show_date', 'begin', 'end', 'language', 'hall', 'price', 'update_time')
    list_filter = ['update_time']
    search_fields = ['cinema_id']


class MinChannelFilter(admin.SimpleListFilter):
    title = 'min_channel'
    parameter_name = 'min_channel'

    def lookups(self, request, model_admin):
        channels = (('mt', 'mt'), ('tb', 'tb'), ('lm', 'lm'))
        return channels

    def queryset(self, request, queryset):
        if self.value() is not None:
            # rs = list()
            # for e in queryset:
            #     if e.min_channel() == self.value():
            #         rs.append(e)
            # return rs
            a = queryset.filter(price_mt=1)
            return a


class PriceFilter(admin.SimpleListFilter):
    title = '未放映渠道'
    parameter_name = 'channel'

    def lookups(self, request, model_admin):
        channels = (('mt', 'mt'), ('tb', 'tb'), ('lm', 'lm'))
        return channels

    def queryset(self, request, queryset):
        channel = self.value()
        if channel is not None:
            if channel == 'mt':
                return queryset.filter(price_mt=10000)
            elif channel == 'tb':
                return queryset.filter(price_tb=10000)
            elif channel == 'lm':
                return queryset.filter(price_lm=10000)


class PriceAdmin(MoviePriceAdmin):
    ordering = ['cinema_id', 'movie_id', 'show_date', 'begin']
    list_display = ('cinema_id', 'movie_id', 'show_date', 'begin', 'end', 'language',  'min_channel',
                    'price_min', 'price_mt', 'price_tb', 'price_lm', 'update_time')
    list_filter = [PriceFilter, 'update_time']
    search_fields = ['cinema_id',]


admin.site.register(MovieMT, MovieChannelAdmin)
admin.site.register(MovieTB, MovieChannelAdmin)
admin.site.register(MovieLM, MovieChannelAdmin)
admin.site.register(MovieDB, MovieChannelAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(MatchMovieLM2DB, MatchMovieAdmin)
admin.site.register(MatchMovieMT2DB, MatchMovieAdmin)
admin.site.register(MatchMovieTB2DB, MatchMovieAdmin)
admin.site.register(PriceLM, MoviePriceAdmin)
admin.site.register(PriceMT, MoviePriceAdmin)
admin.site.register(PriceTB, MoviePriceAdmin)
admin.site.register(Price, PriceAdmin)