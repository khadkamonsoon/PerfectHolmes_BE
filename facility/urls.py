from django.urls import path
from .apis import AroundFacilityListAPI, FacilityListAPI

urlpatterns = [
    path("", FacilityListAPI.as_view()),
    path("around", AroundFacilityListAPI.as_view(), name="facility-around"),
]
