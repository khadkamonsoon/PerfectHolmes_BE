from django.test import TestCase
from django.urls import reverse


class ApartmentAPITest(TestCase):
    def test_apartment_gpt_search_api(self):
        url = reverse("apartment:gpt-apartment-search")
        res = self.client.post(
            url,
            {
                "question": "편의점이 100미터 이내에 있는 준공 10년 미만, 30평 이하, 3억원 이상 아파트를 전월세로 찾고 있습니다."
            },
        )
        print(res.data)

    def test_apartment_search_api(self):
        url = reverse("apartment:apartment-search")
        res = self.client.post(
            url,
            {
                "facility": [  # 시설물 리스트 (type, 거리, 거리단위)
                    {
                        "type": "유치원",
                        "distance": 2000,
                        "unit": "m",
                    },
                    {
                        "type": "편의점",
                        "distance": 100,
                        "unit": "m",
                    },
                    {
                        "type": "은행",
                        "distance": 300,
                        "unit": "m",
                    },
                    {
                        "type": "약국",
                        "distance": 50,
                        "unit": "m",
                    },
                ],
                "apartment": {
                    "room_count": 3,  # 방개수
                    "area": {  # 면적
                        "min": 30,
                        "max": 30,
                        "unit": "평",
                    },
                    "built_year": {  # 준공년도
                        "min": 2012,
                        "max": 2022,
                    },
                    "price": {  # 가격은 만원 단위
                        "min": 3000,
                        "max": 5000,
                        "unit": "만원",
                    },
                },
            },
        )
        print(res.data)
