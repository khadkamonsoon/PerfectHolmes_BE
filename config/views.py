from django.shortcuts import render
from users.utils import decodeJWT


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def main_page(request):
   return render(request, "main.html")


def index_page(request):
    return render(request, "index.html")