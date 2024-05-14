from django.core.management import BaseCommand
from facility.models import Facility
import os, requests, json, environ
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start making convenience store data\n")
        # csv 파일 가져오기
        cu_path = os.path.join(settings.BASE_DIR, "data", "cu.json")

        # 파일 열기 및 JSON 데이터 로드
        with open(cu_path, "r") as file:
            cu_data = json.load(file)

        gs_path = os.path.join(settings.BASE_DIR, "data", "gs.json")

        # 파일 열기 및 JSON 데이터 로드
        with open(gs_path, "r") as file:
            gs_data = json.load(file)

        seven_path = os.path.join(settings.BASE_DIR, "data", "seven.json")

        # 파일 열기 및 JSON 데이터 로드
        with open(seven_path, "r") as file:
            seven_data = json.load(file)

        emart_path = os.path.join(settings.BASE_DIR, "data", "emart24.json")

        # 파일 열기 및 JSON 데이터 로드
        with open(emart_path, "r") as file:
            emart_data = json.load(file)

        # 카카오 API_KEY 가져오기
        environ.Env.read_env(os.path.join(settings.BASE_DIR, ".env"))
        KAKAO_API_KEY = settings.KAKAO_API_KEY

        # Request Header 설정
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

        convenience_store_data = (
            cu_data["장소정보"] + gs_data["장소정보"] + seven_data["장소정보"] + emart_data["장소정보"]
        )

        facility_type = "편의점"

        for convenience_store in convenience_store_data:
            if Facility.objects.filter(
                name=convenience_store["장소명"], type=facility_type
            ).exists():
                continue
            url = (
                "https://dapi.kakao.com/v2/local/search/address.json?query="
                + convenience_store["도로명 주소"]
            )
            api_json = json.loads(str(requests.get(url, headers=headers).text))
            # payload 초기화
            payload = {}
            # 잘못된 데이터 확인
            if api_json["documents"] == []:
                continue
            payload["type"] = facility_type
            payload["name"] = convenience_store["장소명"]
            payload["address"] = convenience_store["도로명 주소"]
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
        self.stdout.write("Make Convenience Store Data is Done. :D\n")
        self.stdout.write(
            "------------------------------------------------------------\n"
        )
