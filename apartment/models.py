from django.db import models
from common.models import CommonModel


class Apartment(CommonModel):
    """Apartment Model Definition"""

    name = models.CharField(max_length=100, verbose_name="아파트명")
    address = models.CharField(max_length=100, verbose_name="주소")
    lat = models.FloatField(verbose_name="위도")
    lng = models.FloatField(verbose_name="경도")
    room_count = models.IntegerField(verbose_name="방 개수", default=1)
    area = models.FloatField(verbose_name="평수", default=1)
    built_year = models.IntegerField(verbose_name="준공년도", default=2020)
    price = models.IntegerField(verbose_name="가격", default=0)
    households = models.IntegerField(verbose_name="세대수", default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "아파트"
        verbose_name_plural = "아파트"
