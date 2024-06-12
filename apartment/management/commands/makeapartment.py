from django.core.management import BaseCommand
from apartment.models import Apartment
import os, requests, json, environ
from django.conf import settings
from api.load_json import load_json


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start making Apartment data\n")

        data = load_json("data", "apartment.json")
        # 카카오 API_KEY 가져오기
        environ.Env.read_env(os.path.join(settings.BASE_DIR, ".env"))
        KAKAO_API_KEY = settings.KAKAO_API_KEY

        # Request Header 설정
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
        apartment_data_list = data["data"]
        for apartment in apartment_data_list:
            address = apartment["시군구"] + apartment["도로명"]
            area = apartment["전용면적(㎡)"] / 3.3
            room_count = 2
            if area > 30:
                room_count = 4
            elif area > 20:
                room_count = 3
            url = "https://dapi.kakao.com/v2/local/search/address.json?query=" + address

            api_json = json.loads(str(requests.get(url, headers=headers).text))

            # payload 초기화
            payload = {}

            # 잘못된 데이터 확인
            if api_json["documents"] == []:
                continue

            payload["address"] = address
            payload["name"] = apartment["단지명"]
            payload["area"] = round(area, 1)
            payload["room_count"] = room_count
            payload["built_year"] = apartment["건축년도"]
            payload["price"] = int(apartment["거래금액(만원)"].replace(",", ""))
            payload["lng"] = api_json["documents"][0]["address"]["x"]
            payload["lat"] = api_json["documents"][0]["address"]["y"]
            # 생성 오류 예외처리
            try:
                Apartment.objects.create(**payload)
                self.stdout.write(".", ending="")
                self.stdout.flush()
            except Exception as e:
                self.stdout.write(f"Error creating Apartment: {e}\n")
        self.stdout.write("\n")
        self.stdout.write("Make Apartment Data is Done. :D\n")
        self.stdout.write(
            "------------------------------------------------------------\n"
        )
