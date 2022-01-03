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

from pick_restful.models import User, Goal, UserGoal
from pick_restful.services import user_record_login, user_get_or_create, jwt_login

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view, permission_classes, authentication_classes

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db.models import Q
import datetime

from pick_restful.selectors import user_goal_info

JWT_authenticator = JWTAuthentication()
def index(request):
        return HttpResponse("연결성공")

class A(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
                response = JWT_authenticator.authenticate(request)
                user , token = response
                print(token['user_id'])
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
                print(token)
                return JsonResponse(token)

from django.core.serializers.json import DjangoJSONEncoder

#############################################나중에 permission_classes = [IsAuthenticated] 로 바꿔야함
class InfoGoalList(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
                queryset = Goal.objects.all().values('id', 'name', 'description', 'icon')
                return JsonResponse(list(queryset), safe=False)

class UserGoalDetail(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
                response = JWT_authenticator.authenticate(request)
                user , token = response

                user = token['user_id']
                user = 'a95a73c3-d1cc-47c3-a557-d3517cd10b49'
                dateCount = request.data['dateCount']
                needColumn = request.data['needColumn']
                startDate = request.data['startDate']
                endDate = datetime.datetime.strptime(startDate, '%Y-%m-%d').date() + datetime.timedelta(days=dateCount-1)
                
                queryset = UserGoal.objects.filter(user=user, select_date__range=[startDate, endDate], active=1).order_by('select_date').values('select_date', 'goal', 'success', 'diary')

                return JsonResponse(user_goal_info(queryset, startDate, dateCount, needColumn), safe=False)


'''
user = 'a95a73c3-d1cc-47c3-a557-d3517cd10b49'
startDate = '2021-12-19'
dateCount = 10
needColumn = ['success', 'diary']
endDate = datetime.datetime.strptime(startDate, '%Y-%m-%d').date() + datetime.timedelta(days=dateCount)
queryset = UserGoal.objects.filter(user=user, select_date__range=[startDate, endDate], active=1).values('select_date', 'goal', 'success', 'diary')
queryset
'''