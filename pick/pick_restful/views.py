from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import redirect
from .models import User#, SocialPlatform
from django.utils import timezone
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


import requests

def index(request):
        return HttpResponse("연결성공")

def a(request):
        return JsonResponse({"aaaa": "aaa"})

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import set_cookie_with_token

from pick_restful.models import User
from pick_restful.services import user_record_login, user_get_or_create

def jwt_login(user: User) -> HttpResponse:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user_record_login(user=user)

        return token


class GoogleLoginView(View): 
        def get(self,request):
                token = request.headers["Authorization"]
                url = 'https://oauth2.googleapis.com/tokeninfo?id_token='
                response = requests.get(url+token)

                accept_status = response.status_code
                if response != 200:
                        print("fail")
                        return JsonResponse({'err_msg': 'failed to asignin'}, status=accept_status)
                
                user_json = response.json()
                user_data = {
                        'email'         : user_json['email'],
                        'first_name'    : user_json['name'],
                        'last_name'     : user_json['name'],
                        'date_birth'    : timezone.localtime(),
                }

                user, _ = user_get_or_create(**user_data)

                token = jwt_login(user=user)
                data = { "accesstoken" : token}
                return JsonResponse(data)