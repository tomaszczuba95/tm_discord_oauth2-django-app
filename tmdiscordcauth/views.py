from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
import requests
# Create your views here.

auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=843491042708029451&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify"
auth_url_tm = "https://api.trackmania.com/oauth/authorize?client_id=28dcbb39593f423da915&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogintm%2Fredirect&response_type=code&scope=&state=test"


def home(request):
    return JsonResponse({"msg": "Siema"})


def discord_login(request: HttpRequest):
    return redirect(auth_url_discord)


def trackmania_login(request: HttpRequest):
    return redirect(auth_url_tm)


def discord_login_redirect(request):
    code = request.GET.get('code')
    print(code)
    user = exchange_code_discord(code)
    return JsonResponse({"user": user, 'YOUR NAME': user['username']})


def trackmania_login_redirected(request):
    code = request.GET.get('code')
    print(code)
    state = request.GET.get('state')
    print(state)
    usertm = exchange_code_trackmania(code)
    return JsonResponse({"gracz tm": usertm})


def exchange_code_discord(code: str):
    data = {
        # https://discord.com/developers/applications
        "client_id": "843491042708029451",
        "client_secret": "AQoufMHsUDMdCaQxUlmfpV6VEtstTZhU",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/oauth2/login/redirect",
        "scope": "identify"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(
        "https://discord.com/api/oauth2/token", data=data, headers=headers)
    print(response)
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get("https://discord.com/api/v6/users/@me", headers={
        'Authorization': 'Bearer %s' % access_token
    })
    print(response)
    user = response.json()
    print(user)
    return user


def exchange_code_trackmania(code: str):
    data = {
        # https://doc.trackmania.com/web-services/auth/
        "grant_type": "authorization_code",
        "client_id": "28dcbb39593f423da915",
        "client_secret": "69b8957caca2bba8e9e74f4472ec0e258c5ff3ce",
        "code": code,
        "redirect_uri": "http://localhost:8000/oauth2/logintm/redirect",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(
        "https://api.trackmania.com/api/access_token", data=data, headers=headers)
    print(response)
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get("https://api.trackmania.com/api/user", headers={
        'Authorization': 'Bearer %s' % access_token
    })
    print(response)
    user = response.json()
    print(user)
    return user
