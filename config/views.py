from django.shortcuts import render
from users.utils import decodeJWT


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def main_page(request):
    if decodeJWT(request.user):
        return render(request, "main.html")
    else : 
        return render(request, "login.html")


def index_page(request):
    return render(request, "index.html")