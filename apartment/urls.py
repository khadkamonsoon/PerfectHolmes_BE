from django.urls import path
from .apis import GPTApartmentSearchAPI, ApartmentSearchAPI

app_name = "apartment"

urlpatterns = [
    path("gpt-search/", GPTApartmentSearchAPI.as_view(), name="gpt-apartment-search"),
    path("search/", ApartmentSearchAPI.as_view(), name="apartment-search"),
]
