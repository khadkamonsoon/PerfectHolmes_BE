from django.core.management import BaseCommand
from facility.models import Facility
import os, requests, json, environ
from django.conf import settings
from api.load_json import load_json


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start making Police Station data\n")

        data = load_json("data", "police_data.json")

        # 카카오 API_KEY 가져오기
        environ.Env.read_env(os.path.join(settings.BASE_DIR, ".env"))
        KAKAO_API_KEY = settings.KAKAO_API_KEY

        # Request Header 설정
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

        center_data_list = data["장소정보"]

        facility_type = "경찰서"

        for center in center_data_list:
            if Facility.objects.filter(name=center["장소명"], type=facility_type).exists():
                continue

            url = (
                "https://dapi.kakao.com/v2/local/search/address.json?query="
                + center["도로명 주소"]
            )
            api_json = json.loads(str(requests.get(url, headers=headers).text))
            # payload 초기화
            payload = {}
            # 잘못된 데이터 확인
            if api_json["documents"] == []:
                continue
            payload["type"] = facility_type
            payload["name"] = center["장소명"]
            payload["address"] = center["도로명 주소"]
            payload["lng"] = api_json["documents"][0]["address"]["x"]
            payload["lat"] = api_json["documents"][0]["address"]["y"]

            # 생성 오류 예외처리
            try:
                Facility.objects.create(**payload)
                self.stdout.write(".", ending="")
                self.stdout.flush()
            except Exception as e:
                self.stdout.write(f"Error creating Facility: {e}\n")
        self.stdout.write("\n")
        self.stdout.write("Make Police Station Data is Done. :D\n")
        self.stdout.write(
            "------------------------------------------------------------\n"
        )
