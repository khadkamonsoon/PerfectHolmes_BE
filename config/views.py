from django.shortcuts import render


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def main_page(request):
    return render(request, "main.html")
