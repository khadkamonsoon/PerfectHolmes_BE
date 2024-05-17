from django.urls import path
from .apis import GPTApartmentSearchAPI

app_name = "apartment"

urlpatterns = [
    path("gpt-search/", GPTApartmentSearchAPI.as_view(), name="gpt-apartment-search"),
]
