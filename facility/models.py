from django.db import models
from common.models import CommonModel


class Facility(CommonModel):
    """Facility Model Definition"""

    class TypeChoices(models.TextChoices):
        kindergarden = ("유치원", "유치원")
        elementary_school = ("초등학교", "초등학교")
        middle_school = ("중학교", "중학교")
        high_school = ("고등학교", "고등학교")
        center = ("주민센터", "주민센터")
        hospital = ("병원", "병원")
        pharmacy = ("약국", "약국")
        bank = ("은행", "은행")
        convenience_store = ("편의점", "편의점")
        bus_stop = ("버스정류장", "버스정류장")

    name = models.CharField(max_length=100, help_text="시설명")
    address = models.CharField(max_length=300, help_text="주소", null=True, blank=True)
    type = models.CharField(
        max_length=50,
        choices=TypeChoices.choices,
        null=True,
        blank=True,
        help_text="시설 구분",
    )
    lat = models.FloatField(help_text="위도")
    lng = models.FloatField(help_text="경도")

    def __str__(self):
        return self.name
