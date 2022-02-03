from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import permission_classes, authentication_classes

from pick_restful.models import User, Goal, UserGoal
from pick_restful.selectors import user_goal_info
from pick_restful.services import user_record_login, user_get_or_create, jwt_login, delete_user, delete_user_undo
from pick_restful.services import get_user_profile, set_user_profile, user_goal_detail_set

import requests, json, datetime

JWT_authenticator = JWTAuthentication()

class GoogleLoginView(APIView):
        permission_classes = [AllowAny]

        def get(self,request):
                token = request.headers["Authorization"]
                url = 'https://oauth2.googleapis.com/tokeninfo?id_token='
                response = requests.get(url+token)
                accept_status = response.status_code
                if accept_status != 200:
                        print("fail")
                        return JsonResponse({'err_msg': 'failed to asignin'}, 
                                                status=accept_status)
                
                user_json = response.json()
                user_data = {
                        'sub'           : user_json['sub'],
                        'social'        : 'google',
                        'email'         : user_json['email'],
                        'first_name'    : user_json['given_name'],
                        'last_name'     : user_json['family_name'],
                        'full_name'     : user_json['name'],
                        'date_birth'    : timezone.localtime(),
                        'last_login'    : timezone.localtime(),
                }
                user, _ = user_get_or_create(**user_data)

                token = jwt_login(user=user)
                print(token)
                return JsonResponse(token)

class InfoGoalList(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
                queryset = Goal.objects.all().extra(
                        select={'activeIcon'    : 'active_icon',
                                'inactiveIcon'  : 'inactive_icon',
                                'mainColor'     : 'main_color',
                                'subColor'      : 'sub_color',
                        }).values('id', 'name', 'description', 'activeIcon',
                                'inactiveIcon', 'mainColor', 'subColor')
                return JsonResponse(list(queryset), safe=False)

class UserGoalDetailGet(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
                response = JWT_authenticator.authenticate(request)
                user , token = response
                user = token['user_id']
                dateCount = request.data['dateCount']
                needColumn = request.data['needColumn']
                startDate = request.data['startDate']
                endDate = datetime.datetime.strptime(startDate, '%Y-%m-%d').date() + datetime.timedelta(days=dateCount-1)
                queryset = UserGoal.objects.filter(
                        user=user, 
                        select_date__range=[startDate, endDate], 
                        active=1).values('select_date', 'goal', 'success', 'diary')
                return JsonResponse(
                        user_goal_info(
                                queryset, 
                                startDate, 
                                dateCount, 
                                needColumn), 
                        safe=False)

class UserGoalDetailSet(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
                response = JWT_authenticator.authenticate(request)
                user , token = response

                user = token['user_id']
                date = request.data['date']
                updateColumn = request.data['updateColumn']
                userGoalList = request.data['userGoalList']
                user_goal_detail_set(date, user, userGoalList, updateColumn)

                return JsonResponse({"success" : "success"}, safe=False)

class UserProfile(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
                response = JWT_authenticator.authenticate(request)
                user , token = response
                user = token['user_id']

                return JsonResponse(
                        get_user_profile(user), 
                        safe=False)

        def post(self, request):
                response = JWT_authenticator.authenticate(request)
                user , token = response
                user = token['user_id']
                set_user_profile(user=user, **request.data)
                return JsonResponse({'success':'success'}, 
                        safe=False)
                
class UserDelete(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
                response = JWT_authenticator.authenticate(request)
                user , token = response
                user = token['user_id']
                delete_user(user=user)
                return JsonResponse({'success':'success'}, 
                        safe=False)
                
class UserDeleteUndo(APIView):
        permission_classes = [AllowAny]

        def post(self, request):
                user = request.data['uuid']
                delete_user_undo(user=user)
                return JsonResponse({'success':'success'}, 
                        safe=False)