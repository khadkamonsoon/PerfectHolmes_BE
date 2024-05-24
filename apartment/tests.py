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
                "facility": [
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
                    "room_count": 3,
                    "area": 30,
                    "built_year": {
                        "min": 2012,
                        "max": 2022,
                    },
                    "price": {
                        "min": 300000000,
                        "max": 500000000,
                    },
                    "households": 100,
                },
            },
        )
        print(res.data)
