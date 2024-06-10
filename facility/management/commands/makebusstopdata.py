from django.core.management import BaseCommand
from facility.models import Facility
import os, json
from django.conf import settings
from api.load_json import load_json


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start making bus stop data\n")

        data = load_json("data", "bus.json")

        bus_stop_data_list = data["장소정보"]

        facility_type = "버스정류장"

        for bus_stop in bus_stop_data_list:

            if Facility.objects.filter(
                name=bus_stop["장소명"], type=facility_type
            ).exists():
                continue

            # payload 초기화
            payload = {}

            # 잘못된 데이터 확인
            payload["type"] = facility_type
            payload["name"] = bus_stop["장소명"]
            payload["lng"] = bus_stop["경도"]
            payload["lat"] = bus_stop["위도"]

            # 생성 오류 예외처리
            try:
                Facility.objects.create(**payload)
                self.stdout.write(".", ending="")
                self.stdout.flush()
            except Exception as e:
                self.stdout.write(f"Error creating Facility: {e}\n")
        self.stdout.write("\n")
        self.stdout.write("Make Bus Stop Data is Done. :D\n")
        self.stdout.write(
            "------------------------------------------------------------\n"
        )
