from django.contrib import admin

from base.models.city import CityMT, CityTB, CityLM, City


class CityChannelAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('id', 'g', 'name', 'update_time')
    search_fields = ['name']
    list_filter = ['g', 'update_time']


class CityAdmin(admin.ModelAdmin):
    ordering = ['id_mt']
    list_display = ('id_mt', 'id_tb', 'id_lm', 'g', 'name', 'update_time')
    search_fields = ['name']
    list_filter = ['g', 'update_time']


admin.site.register(CityMT, CityChannelAdmin)
admin.site.register(CityLM, CityChannelAdmin)
admin.site.register(CityTB, CityChannelAdmin)
admin.site.register(City, CityAdmin)