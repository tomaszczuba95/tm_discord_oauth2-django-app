from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import DiscordUser, TrackmaniaUser
import requests
import base64
import os
import http.client
import json
from rest_framework import viewsets
from .serializers import TrackmaniaUserSerializer
from decouple import config
# Create your views here.
auth_url_discord_local = "https://discord.com/api/oauth2/authorize?client_id=" + \
    config('DISCORD_CLIENT_ID') + \
    "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify"

auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=" + \
    config('DISCORD_CLIENT_ID') + \
    "&redirect_uri=https%3A%2F%2Ftm-discord-authorization.herokuapp.com%2Foauth2%2Flogin%2Fredirect&response_type=code&scope=identify"

auth_url_tm_local = "https://api.trackmania.com/oauth/authorize?client_id=" + \
    config('TRACKMANIA_API_ID') + \
    "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Flogintm%2Fredirect&response_type=code&scope=&state=test"

auth_url_tm = "https://api.trackmania.com/oauth/authorize?client_id=" + \
    config('TRACKMANIA_API_ID') + \
    "&redirect_uri=https%3A%2F%2Ftm-discord-authorization.herokuapp.com%2Foauth2%2Flogintm%2Fredirect&response_type=code&scope=&state=tm"

home_url = "http://127.0.0.1:8000/oauth2/login/redirect"


# API

class TrackmaniaUserViewSet(viewsets.ModelViewSet):
    queryset = TrackmaniaUser.objects.all()
    serializer_class = TrackmaniaUserSerializer

# DISCORD


@login_required(login_url="https://tm-discord-authorization.herokuapp.com/")
def get_authenticated_user(request):
    return JsonResponse({"msg": "Authenticated", "user": request.user.discord_id})


def discord_login(request: HttpRequest):
    return redirect(auth_url_discord)


def discord_login_redirect(request):
    code = request.GET.get('code')
    user = exchange_code_discord(code)
    discord_user = authenticate(request, user=user)
    discord_user = discord_user.first()
    login(request, discord_user)
    try:
        find_relation = TrackmaniaUser.objects.filter(
            linked_discord=request.user)
        if len(find_relation) == 0:
            is_related = False
        else:
            is_related = True
        find_relation = list(find_relation).pop()
    except:
        is_related = False
        find_relation = "Couldnt find a relation"
    # return redirect(trackmania_login)
    return render(request, 'details.html', {'is_related': is_related,
                                            'find_relation': find_relation})


def exchange_code_discord(code: str):
    data = {
        # https://discord.com/developers/applications
        "client_id": config('DISCORD_CLIENT_ID'),
        "client_secret": config('DISCORD_CLIENT_SECRET'),
        "grant_type": "authorization_code",
        "code": code,
        # "redirect_uri": "http://localhost:8000/oauth2/login/redirect",
        "redirect_uri": "https://tm-discord-authorization.herokuapp.com/oauth2/login/redirect",
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


@login_required(login_url="https://tm-discord-authorization.herokuapp.com/")
def trackmania_login(request: HttpRequest):
    return redirect(auth_url_tm)


@login_required(login_url="https://tm-discord-authorization.herokuapp.com/")
def trackmania_login_redirected(request):
    code = request.GET.get('code')
    print(code)
    state = request.GET.get('state')
    print(state)
    usertm = exchange_code_trackmania(code)
    user_id = [request.user.discord_id]
    print("user id: ", user_id)
    user = request.user
    new_tm_user = TrackmaniaUser.objects.create_new_trackmania_user(request,
                                                                    usertm)
    # return JsonResponse({"gracz tm": usertm, "user": request.user.discord_id})
    return render(request, "finish.html")


def exchange_code_trackmania(code: str):
    data = {
        # https://doc.trackmania.com/web-services/auth/
        "grant_type": "authorization_code",
        "client_id": config('TRACKMANIA_API_ID'),
        "client_secret": config('TRACKMANIA_API_SECRET'),
        "code": code,
        # "redirect_uri": "http://localhost:8000/oauth2/logintm/redirect",
        "redirect_uri": "https://tm-discord-authorization.herokuapp.com/oauth2/logintm/redirect",
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
