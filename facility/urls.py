from django.urls import path
from .apis import AroundFacilityListAPI

urlpatterns = [
    path("around", AroundFacilityListAPI.as_view(), name="facility-around"),
]
