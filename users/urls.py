from django.urls import path
from .apis import LoginAPI, SignupAPI, LogoutAPI, RefreshAPI

urlpatterns = [
    path("login", LoginAPI.as_view(), name="login"),
    path("signup", SignupAPI.as_view(), name="signup"),
    path("logout", LogoutAPI.as_view(), name="logout"),
    path("refresh", RefreshAPI.as_view(), name="refresh"),
]
