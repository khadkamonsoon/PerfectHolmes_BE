import os, json
from django.conf import settings


def load_json(dir, file_name):
    file_path = os.path.join(settings.BASE_DIR, dir, file_name)

    # 파일 열기 및 JSON 데이터 로드, utf-8로 인코딩
    with open(file_path, "r", encoding="UTF-8") as file:
        return json.load(file)
