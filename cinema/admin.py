
from django.contrib import admin

from cinema.models.cinema import CinemaMT, CinemaTB, CinemaLM, Cinema
from cinema.models.match import MatchCinemaTB2MT, MatchCinemaLM2MT


class MinPriceFilter(admin.SimpleListFilter):
    title = '影院最低价'
    parameter_name = 'min_price'

    def lookups(self, request, model_admin):
        price = (('=0', '=0'), ('<20 and >0', '<20 and >0'), ('<30 and >=20', '<30 and >=20'), ('>=30', '>=30'))
        return price

    def queryset(self, request, queryset):
        price = self.value()
        if price is not None:
            if price == '=0':
                return queryset.filter(min_price__lt=1)
            elif price == '<20 and >0':
                return queryset.filter(min_price__lt=20, min_price__gte=1)
            elif price == '<30 and >=20':
                return queryset.filter(min_price__lt=30, min_price__gte=20)
            elif price == '>=30':
                return queryset.filter(min_price__gte=30)


class CinemaChannelAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'city', 'addr', 'min_price', 'price_update_time', 'create_time', 'update_time')
    search_fields = ['id', 'name', 'addr']
    list_filter = ['city', 'district', MinPriceFilter,'update_time']


class CinemaFilter(admin.SimpleListFilter):
    title = '未匹配渠道'
    parameter_name = 'channel'

    def lookups(self, request, model_admin):
        channels = (('mt', 'mt'), ('tb', 'tb'), ('lm', 'lm'))
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


class CinemaAdmin(admin.ModelAdmin):
    ordering = ['id_mt']
    list_display = ('id_mt', 'id_tb', 'id_lm', 'name', 'city', 'addr','min_price', 'create_time', 'update_time')
    search_fields = ['id_mt', 'id_tb', 'id_lm', 'name', 'addr']
    list_filter = ['city', 'district', MinPriceFilter, CinemaFilter, 'update_time']


class MatchCinemaAdmin(admin.ModelAdmin):
    ordering = ['id_mt']
    list_display = ('id_mt', 'id_matched', 'match_type', 'match_score', 'match_step', 'is_delete', 'update_time')
    list_filter = ['match_type', 'match_step', 'match_score', 'match_step', 'update_time']


admin.site.register(CinemaMT, CinemaChannelAdmin)
admin.site.register(CinemaTB, CinemaChannelAdmin)
admin.site.register(CinemaLM, CinemaChannelAdmin)
admin.site.register(MatchCinemaTB2MT, MatchCinemaAdmin)
admin.site.register(MatchCinemaLM2MT, MatchCinemaAdmin)
admin.site.register(Cinema, CinemaAdmin)


