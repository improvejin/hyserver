import json

from django.http import HttpResponse

# Create your views here.
from movie.service import MovieService


service = MovieService()


def get_movies(request):
    """获取电影院放映的影片信息"""
    cinema_id = int(request.GET.get('cinemaId'))
    # cinema_id = 6
    movies = service.get_movies_by_cinema(cinema_id)
    res = list()
    for m in movies:
        res.append(m.to_dict())
    json_str = json.dumps(res)
    return HttpResponse(json_str, content_type="application/json")


def get_movie_price(request, movie_id):
    cinema_id = int(request.GET.get('cinemaId'))
    # cinema_id = 6
    res = list()
    shows = service.get_movie_price(cinema_id, movie_id)
    for date in sorted(shows.keys()):
        day_show = dict()
        day_show['date'] = date.strftime('%m-%d').lstrip('0')
        day_schedules = list()
        for schedule in shows[date]:
            day_schedules.append(schedule.to_dict())
        day_show['schedules'] = day_schedules
        res.append(day_show)
    json_str = json.dumps(res)
    return HttpResponse(json_str, content_type="application/json")
    return json_str
