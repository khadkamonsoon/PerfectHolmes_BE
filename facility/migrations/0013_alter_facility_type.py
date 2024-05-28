# Generated by Django 3.2 on 2024-05-26 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("facility", "0012_alter_facility_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facility",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("유치원", "유치원"),
                    ("초등학교", "초등학교"),
                    ("중학교", "중학교"),
                    ("고등학교", "고등학교"),
                    ("주민센터", "주민센터"),
                    ("치과", "치과"),
                    ("내과", "내과"),
                    ("보건소", "보건소"),
                    ("외과", "외과"),
                    ("산부인과", "산부인과"),
                    ("종합병원", "종합병원"),
                    ("비뇨기과", "비뇨기과"),
                    ("피부과", "피부과"),
                    ("한의원", "한의원"),
                    ("조산원", "조산원"),
                    ("정신건강학과", "정신건강학과"),
                    ("재활의학과", "재활의학과"),
                    ("이비인후과", "이비인후과"),
                    ("요양병원", "요양병원"),
                    ("안과", "안과"),
                    ("신경과", "신경과"),
                    ("소아청소년과", "소아청소년과"),
                    ("성형외과", "성형외과"),
                    ("가정의학과", "가정의학과"),
                    ("약국", "약국"),
                    ("은행", "은행"),
                    ("편의점", "편의점"),
                    ("버스정류장", "버스정류장"),
                    ("주유소", "주유소"),
                    ("노인복지시설", "노인복지시설"),
                    ("볼링장", "볼링장"),
                    ("영화관", "영화관"),
                    ("헬스장", "헬스장"),
                    ("아동복지시설", "아동복지시설"),
                    ("전기차충전소", "전기차충전소"),
                ],
                help_text="시설 구분",
                max_length=50,
                null=True,
            ),
        ),
    ]
