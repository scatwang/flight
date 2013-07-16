#coding:utf8
from django.db import models

class Airport(models.Model):
    class Meta:
        verbose_name = "机场"
    def __unicode__(self):
        return "%s.%s(%s-%s)" % (self.id, self.name, self.code, self.ICAO_code)
    code = models.CharField(max_length=3)
    ICAO_code = models.CharField(max_length=4)
    name = models.CharField(max_length=500)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    domestic_flights = models.IntegerField()
    intl_flights = models.IntegerField()

    lat = models.FloatField()
    lng = models.FloatField()
class AirlineCorporation(models.Model):
    class Meta:
        verbose_name = "航空公司"
    def __unicode__(self):
        return "%s-%s" % (self.code, self.name)
    name  = models.CharField(max_length=1024)
    code = models.CharField(max_length=3)
class AirlineInfo(models.Model):
    class Meta:
        verbose_name = "航线信息"

    flight_no = models.CharField(max_length=10)
    is_codeshare = models.BooleanField()
    plane_model = models.CharField(max_length=10)

    depart_airport = models.CharField(max_length=3)
    arrive_airport = models.CharField(max_length=3)
    depart_time = models.CharField(max_length=10)
    arrive_time = models.CharField(max_length=10)

    valid_begin = models.DateField()
    valid_end = models.DateField()
    weekly_schedule = models.CharField(max_length=7)

    have_meal = models.BooleanField()
    stop_count = models.IntegerField()

    last_update_time = models.DateTimeField(auto_now_add=True, blank=True)

