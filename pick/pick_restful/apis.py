from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

import requests, json

from pick_restful.models import User, Goal
from pick_restful.services import user_record_login, user_get_or_create, jwt_login

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view, permission_classes, authentication_classes

from rest_framework_simplejwt.authentication import JWTAuthentication

JWT_authenticator = JWTAuthentication()
def index(request):
        return HttpResponse("연결성공")

class A(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
                response = JWT_authenticator.authenticate(request)
                user , token = response
                print(token.payload)
                return JsonResponse({"message": "Hello, world!"})

        def post(self, request):
                response = JWT_authenticator.authenticate(request)
                user , token = response
                print(token.payload)
                return JsonResponse({"message2": "Hello, world!"})


class GoogleLoginView(APIView):
        permission_classes = [AllowAny]

        def get(self,request):
                token = request.headers["Authorization"]
                url = 'https://oauth2.googleapis.com/tokeninfo?id_token='
                response = requests.get(url+token)
                accept_status = response.status_code
                if accept_status != 200:
                        print("fail")
                        return JsonResponse({'err_msg': 'failed to asignin'}, status=accept_status)
                
                user_json = response.json()
                user_data = {
                        'sub'           : user_json['sub'],
                        'social'        : 'google',
                        'email'         : user_json['email'],
                        'first_name'    : user_json['name'],
                        'last_name'     : user_json['name'],
                        'date_birth'    : timezone.localtime(),
                        'last_login'    : timezone.localtime(),
                }

                user, _ = user_get_or_create(**user_data)

                token = jwt_login(user=user)
                return JsonResponse(token)

from django.core.serializers.json import DjangoJSONEncoder

class InfoGoalList(APIView):
        permission_classes = [AllowAny]

        def get(self, request):
                queryset = Goal.objects.all().values('name', 'description', 'icon')
                queryset = list(queryset)
                return JsonResponse(queryset, safe=False)