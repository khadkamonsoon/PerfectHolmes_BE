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
