from django.urls import path
from .apis import LoginAPI

urlpatterns = [
    path("login/", LoginAPI.as_view(), name="login"),
]
