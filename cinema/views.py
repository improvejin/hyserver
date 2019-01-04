
from django.http import HttpResponse

import json
from base.log import logger

from cinema.service import CinemaService

service = CinemaService()


def get_cinemas(request):
    logger.debug(request)
    city = request.GET.get('city', default='上海')
    district = request.GET.get('district', default='闵行区')
    lat_lng = request.GET.get('location', default='31.162025585106374,121.35651573016243')
    sort_by = request.GET.get('sortBy', default='distance')
    page = int(request.GET.get('page', default=0))
    page_size = int(request.GET.get('size', default=10))
    cinemas = service.get_cinemas_by_location(city, lat_lng, page, page_size)
    json_str = json.dumps(cinemas)
    return HttpResponse(json_str, content_type="application/json")


def search_cinemas(request):
    city = request.GET.get('city', default='上海')
    lat_lng = request.GET.get('location', default='31.162025585106374,121.35651573016243')
    page = int(request.GET.get('page', default=0))
    page_size = int(request.GET.get('size', default=10))
    cinemas = service.get_cinemas_by_location(city, lat_lng, page, page_size)
    json_str = json.dumps(cinemas)
    return HttpResponse(json_str, content_type="application/json")