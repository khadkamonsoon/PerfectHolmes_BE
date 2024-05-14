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
        dental_clinic = ("치과", "치과")
        internal_medicine = ("내과", "내과")
        public_health_center = ("보건소", "보건소")
        surgery = ("외과", "외과")
        obstetrics_gynecology = ("산부인과", "산부인과")
        general_hospital = ("종합병원", "종합병원")
        urology = ("비뇨기과", "비뇨기과")
        dermatology = ("피부과", "피부과")
        oriental_clinic = ("한의원", "한의원")
        maternity_hospital = ("조산원", "조산원")
        mental_health_clinic = ("정신건강학과", "정신건강학과")
        rehabilitation_clinic = ("재활의학과", "재활의학과")
        orthopedic_surgery = ("이비인후과", "이비인후과")
        nursing_hospital = ("요양병원", "요양병원")
        ophthalmology = ("안과", "안과")
        neurology = ("신경과", "신경과")
        pediatrics = ("소아청소년과", "소아청소년과")
        plastic_surgery = ("성형외과", "성형외과")
        family_medicine = ("가정의학과", "가정의학과")
        pharmacy = ("약국", "약국")
        bank = ("은행", "은행")
        convenience_store = ("편의점", "편의점")
        bus_stop = ("버스정류장", "버스정류장")
        gas_station = ("주유소", "주유소")
        welfare_center = ("노인복지시설", "노인복지시설")
        bowling_club = ("볼링장", "볼링장")

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
