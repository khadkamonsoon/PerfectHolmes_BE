from django.core.management import BaseCommand
from facility.models import Facility
import os, requests, json, environ
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        # csv 파일 가져오기
        file_path = os.path.join(settings.BASE_DIR, "data", "welfare_center.json")

        # 파일 열기 및 JSON 데이터 로드
        with open(file_path, "r") as file:
            data = json.load(file)
        # 카카오 API_KEY 가져오기
        environ.Env.read_env(os.path.join(settings.BASE_DIR, ".env"))
        KAKAO_API_KEY = settings.KAKAO_API_KEY

        # Request Header 설정
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

        welfare_center_data = data["장소정보"]

        facility_type = "노인복지시설"

        for welfare_center in welfare_center_data:
            if Facility.objects.filter(
                name=welfare_center["장소명"], type=facility_type
            ).exists():
                continue
            url = (
                "https://dapi.kakao.com/v2/local/search/address.json?query="
                + welfare_center["도로명 주소"]
            )
            api_json = json.loads(str(requests.get(url, headers=headers).text))
            # payload 초기화
            payload = {}
            # 잘못된 데이터 확인
            if api_json["documents"] == []:
                continue
            payload["type"] = facility_type
            payload["name"] = welfare_center["장소명"]
            payload["address"] = welfare_center["도로명 주소"]
            payload["lng"] = api_json["documents"][0]["address"]["x"]
            payload["lat"] = api_json["documents"][0]["address"]["y"]

            # 생성 오류 예외처리
            try:
                Facility.objects.create(**payload)
            except:
                pass
        print("Make Welfare Center Data is Done. :D")
