from django.core.management import BaseCommand
from facility.models import Facility
import pandas as pd
import os, requests, json, environ
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        # csv 파일 가져오기
        path = os.path.join(settings.BASE_DIR, "school_data.csv")
        df = pd.read_csv(path)
        # amazon instance에 ftp 로 업로드
        # docker cp 명령어로 container 에 복사
        # container 에서 파일 확인 후 명령어 실행
        # container 재실행
        # amazon instance 에 파일 삭제

        # 카카오 API_KEY 가져오기
        environ.Env.read_env(os.path.join(settings.BASE_DIR, ".env"))
        KAKAO_API_KEY = settings.KAKAO_API_KEY

        # Request Header 설정
        headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

        # csv 데이터 순회
        for item in df.itertuples():
            # 좌표 변환 API 호출
            url = "https://dapi.kakao.com/v2/local/search/address.json?query=" + item[4]
            api_json = json.loads(str(requests.get(url, headers=headers).text))
            # payload 초기화
            payload = {}
            # 잘못된 데이터 확인
            if api_json["documents"] == []:
                continue

            # 학교 구분
            if "유치원" in str(item[1]):
                payload["type"] = "유치원"
            elif "초등학교" in str(item[1]):
                payload["type"] = "초등학교"
            elif "중학교" in str(item[1]):
                payload["type"] = "중학교"
            elif "고등학교" in str(item[1]):
                payload["type"] = "고등학교"
            else:
                continue

            payload["name"] = item[1]
            payload["address"] = item[4]
            # 위도 경도 설정
            payload["lng"] = api_json["documents"][0]["address"]["x"]
            payload["lat"] = api_json["documents"][0]["address"]["y"]

            # 생성 오류 예외처리
            try:
                if not Facility.objects.filter(
                    name=payload["name"], type=payload["type"]
                ).exists():
                    Facility.objects.create(**payload)
            except:
                pass
        print("Make School Data is Done. :D")
