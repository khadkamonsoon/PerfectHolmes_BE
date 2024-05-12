from django.db import models
from common.models import CommonModel


class Apartment(CommonModel):
    """Apartment Model Definition"""

    name = models.CharField(max_length=100, verbose_name="아파트명")
    address = models.CharField(max_length=100, verbose_name="주소")
    lat = models.FloatField(verbose_name="위도")
    lng = models.FloatField(verbose_name="경도")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "아파트"
        verbose_name_plural = "아파트"
