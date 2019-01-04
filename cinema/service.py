import pymysql

from cinema.models.cinema import Cinema
from hyserver import settings
from base.log import logger

HOST = settings.DATABASES['default']['HOST']
DB = settings.DATABASES['default']['NAME']
USER = settings.DATABASES['default']['USER']
PWD = settings.DATABASES['default']['PASSWORD']


class CinemaService(object):

    def __init__(self):
        self.conn = pymysql.connect(HOST, USER, PWD, DB)
        self.conn.set_charset('utf8')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_cinemas_by_location(self, city, lat_lng, page=0, page_size=10):
        start = page*page_size
        sql = 'select id_mt, name, addr, lat_lng, min_price from cinema where city="{}" and min_price>0 order by st_distance(Point({}),location) asc limit {}, {}'.format(city, lat_lng, start, page_size)
        logger.debug(sql)
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()
        cinemas = list()
        for r in rs:
            c = dict()
            c['id'] = r[0]
            c['name'] = r[1]
            c['addr'] = r[2]
            c['lat_lng'] = r[3]
            c['min_price'] = r[4]
            cinemas.append(c)
        self.conn.commit()
        return cinemas

    def get_cinemas_by_price(self, city, district=None):
        cinemas = list()
        rs = Cinema.objects.filter(city=city, min_price__gt=0)
        if district is not None:
            rs = rs.filter(district=district)
        rs = rs.order_by('min_price')
        for r in rs:
            cinemas.append(r.to_dict())
        return cinemas


if __name__ == '__main__':
    service = CinemaService()
    #cinemas = service.get_cinemas_by_location('上海', '31.1604447050825,121.357030810457')
    cinemas = service.get_cinemas_by_price('上海')
    print(cinemas)