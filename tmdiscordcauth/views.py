from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
import requests
import base64
import os
import http.client
import json
# Create your views here.

auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=" + \
    os.environ['DISCORD_CLIENT_ID'] + \
    "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify"
auth_url_tm = "https://api.trackmania.com/oauth/authorize?client_id=" + \
    os.environ['TRACKMANIA_API_ID'] + \
    "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogintm%2Fredirect&response_type=code&scope=&state=test"


def home(request):
    return JsonResponse({"msg": "Siema"})

# DISCORD


def discord_login(request: HttpRequest):
    return redirect(auth_url_discord)


def discord_login_redirect(request):
    code = request.GET.get('code')
    print(code)
    user = exchange_code_discord(code)
    return JsonResponse({"user": user, 'YOUR NAME': user['username']})


def exchange_code_discord(code: str):
    data = {
        # https://discord.com/developers/applications
        "client_id": os.environ['DISCORD_CLIENT_ID'],
        "client_secret": os.environ['DISCORD_CLIENT_SECRET'],
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

# TRACKMANIA


def trackmania_login(request: HttpRequest):
    return redirect(auth_url_tm)


def trackmania_login_redirected(request):
    code = request.GET.get('code')
    print(code)
    state = request.GET.get('state')
    print(state)
    usertm = exchange_code_trackmania(code)
    return JsonResponse({"gracz tm": usertm})


def exchange_code_trackmania(code: str):
    data = {
        # https://doc.trackmania.com/web-services/auth/
        "grant_type": "authorization_code",
        "client_id": os.environ['TRACKMANIA_API_ID'],
        "client_secret": os.environ['TRACKMANIA_API_SECRET'],
        "code": code,
        "redirect_uri": "http://localhost:8000/oauth2/logintm/redirect",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # https://api.trackmania.com/doc
    # JSON: account_id and display_name.
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


def nadeo_services_access(request):
    ubi_ticket = ubiservices_level0()
    print(ubi_ticket)
    nadeo_token = nadeo_accesstoken_level1(ubi_ticket)
    print(nadeo_token['accessToken'])
    services = nadeo_services(nadeo_token['accessToken'])
    return JsonResponse({"level 0 ticket": ubi_ticket, "level 1 ticket": nadeo_token, "level 2 services": services})


def ubiservices_level0():
    conn = http.client.HTTPSConnection("public-ubiservices.ubi.com")
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        # 'Basic base64.b64encode(b'email:password').decode()',
        'Authorization': 'Basic dG9tYXN6ZGphbmdvYXBwQGdtYWlsLmNvbTpUcmFja21hbmlhMTIz',
        'Ubi-AppId': '86263886-327a-4328-ac69-527f0d20a237'
    }
    conn.request("POST", "/v3/profiles/sessions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decoded_data = data.decode("utf-8")
    response = json.loads(decoded_data)
    return response['ticket']


def nadeo_accesstoken_level1(ticket):
    headers = {
        "Authorization": "ubi_v1 t=" + ticket
    }
    nadeo_accesstoken = requests.post(
        "https://prod.trackmania.core.nadeo.online/v2/authentication/token/ubiservices", headers=headers
    )
    return nadeo_accesstoken.json()


def nadeo_services(token):
    payload = {
        'audience': 'NadeoClubServices'
    }
    headers = {
        "Authorization": "nadeo_v1 t=" + token,
    }
    nadeo_services = requests.post(
        "https://prod.trackmania.core.nadeo.online/v2/authentication/token/nadeoservices", headers=headers, data=payload
    )
    return nadeo_services.json()
