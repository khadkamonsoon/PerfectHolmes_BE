from django.core.management import BaseCommand
from facility.models import Facility
import os, requests, json, environ
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        # csv 파일 가져오기
        file_path = os.path.join(settings.BASE_DIR, "data", "academy_data.json")

        # 파일 열기 및 JSON 데이터 로드
        with open(file_path, "r") as file:
            data = json.load(file)
        # 카카오 API_KEY 가져오기
        environ.Env.read_env(os.path.join(settings.BASE_DIR, ".env"))
        KAKAO_API_KEY = settings.KAKAO_API_KEY

        # Request Header 설정
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
        facility_type = "학원"
        academy_data_list = data
        for academy in academy_data_list:
            if "지역" in academy or "계열" in academy:
                name = academy.get("지역")
                address = academy.get("계열")
            else:
                name = academy.get("장소명")
                address = academy.get("주소")
            if Facility.objects.filter(name=name, type=facility_type).exists():
                continue
            url = "https://dapi.kakao.com/v2/local/search/address.json?query=" + address
            api_json = json.loads(str(requests.get(url, headers=headers).text))

            # payload 초기화
            payload = {}

            # 잘못된 데이터 확인
            if api_json["documents"] == []:
                continue
            payload["type"] = facility_type
            payload["name"] = name
            payload["address"] = address
            payload["lng"] = api_json["documents"][0]["address"]["x"]
            payload["lat"] = api_json["documents"][0]["address"]["y"]

            # 생성 오류 예외처리
            try:
                Facility.objects.create(**payload)
            except:
                pass
        print("Make Academy Data is Done. :D")
