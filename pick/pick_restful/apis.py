from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import permission_classes, authentication_classes

from pick_restful.models import User, Goal, UserGoal
from pick_restful.selectors import user_goal_info
from pick_restful.services import user_record_login, user_get_or_create, jwt_login, delete_user, delete_user_undo
from pick_restful.services import get_user_profile, guest_create, set_user_profile, user_goal_detail_set, guest_get, user_link

import requests, json, datetime, jwt

JWT_authenticator = JWTAuthentication()
        
class GoogleLoginView(APIView):
        permission_classes = [AllowAny]

        def get(self,request):
                try:
                        token = request.headers["Authorization"]
                except KeyError:
                        print("error : not found Authorization in headers")
                        return JsonResponse({'err_msg': 'not found Authorization in headers'})
                
                url = 'https://oauth2.googleapis.com/tokeninfo?id_token='
                response = requests.get(url+token)
                accept_status = response.status_code
                if accept_status != 200:
                        print("err_msg : oauth2.googleapis.com login fail")
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
                        'date_birth'    : datetime.datetime.now(),
                        'last_login'    : datetime.datetime.now(),
                }
                user, _ = user_get_or_create(**user_data)

                token = jwt_login(user=user)
                print(token)
                return JsonResponse(token)
        
class GuestLoginView(APIView):
        permission_classes = [AllowAny]

        def post(self, request):
                try:
                        user = request.data["Authorization"]
                except KeyError:
                        print("error : not found Authorization in headers")
                        return JsonResponse({'err_msg': 'not found Authorization in headers'})
                
                user, msg = guest_get(user)
                if msg == "success":
                        token = jwt_login(user=user)
                        print(token)
                        return JsonResponse(token, status=200)
                else:
                        return JsonResponse({'err_msg': msg}, status=400)

class InfoGoalList(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
                
                # need to go service
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
                
                # need to go service.py
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
                success = set_user_profile(user=user, **request.data)
                if success:
                        return JsonResponse({'success':'success'}, safe=False, status=200)
                else:
                        return JsonResponse({'fail':'fail'}, safe=False, status=400)
                
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
                
class UserCreate(APIView):
        permission_classes = [AllowAny]

        def get(self, request):
                user = guest_create()
                
                return JsonResponse({"idToken": user.id})
        
class GoogleLink(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
                try:
                        token = request.data["googleIdToken"]
                except KeyError:
                        print("error : not found googleIdToken in body")
                        return JsonResponse({'err_msg': 'not found googleIdToken in body'})
                
                try:
                        user = request.data["guestIdToken"]
                except KeyError:
                        print("error : not found guestIdToken in body")
                        return JsonResponse({'err_msg': 'not found guestIdToken in body'})
                
                url = 'https://oauth2.googleapis.com/tokeninfo?id_token='
                response = requests.get(url+token)
                accept_status = response.status_code
                if accept_status != 200:
                        print("err_msg : oauth2.googleapis.com login fail")
                        return JsonResponse({'err_msg': 'failed to asignin'}, 
                                                status=accept_status)
                
                user_json = response.json()
                user_data = {
                        'platform'      : 'google',
                        'id'            : user,
                        'sub'           : user_json['sub'],
                        'email'         : user_json['email'],
                        'first_name'    : user_json['given_name'],
                        'last_name'     : user_json['family_name'],
                        'full_name'     : user_json['name'],
                }
                user, msg = user_link(**user_data)
                
                if user:
                        return JsonResponse({'success': 1, 'msg': msg}, status=200)
                else:
                        return JsonResponse({'success': 0, 'msg': msg}, status=400)

class AppleLoginView(APIView):
        permission_classes = [AllowAny]

        def get(self,request):
                try:
                        token = request.headers["idToken"]
                except KeyError:
                        print("error : not found idToken in headers")
                        return JsonResponse({'err_msg': 'not found idToken in headers'})
                
                try:
                        first_name = request.headers["firstName"]
                except KeyError:
                        print("error : not found firstName in headers")
                        return JsonResponse({'err_msg': 'not found firstName in headers'})
                
                try:
                        last_name = request.headers["lastName"]
                except KeyError:
                        print("error : not found lastName in headers")
                        return JsonResponse({'err_msg': 'not found lastName in headers'})
                
                
                
                data = jwt.decode(token, options={'verify_signature': False})
                
                user_data = {
                        'sub'           : data['sub'],
                        'social'        : 'apple',
                        'email'         : data['email'],
                        'first_name'    : first_name,
                        'last_name'     : last_name,
                        'full_name'     : last_name + ' ' + first_name,
                        'date_birth'    : datetime.datetime.now(),
                        'last_login'    : datetime.datetime.now(),
                }
                user, _ = user_get_or_create(**user_data)
                
                token = jwt_login(user=user)
                print(token)
                return JsonResponse(token)
                   
class AppleLink(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
                try:
                        token = request.data["appleidToken"]
                except KeyError:
                        print("error : not found idToken in headers")
                        return JsonResponse({'err_msg': 'not found idToken in headers'})
                
                try:
                        first_name = request.data["firstName"]
                except KeyError:
                        print("error : not found firstName in headers")
                        return JsonResponse({'err_msg': 'not found firstName in headers'})
                
                try:
                        last_name = request.data["lastName"]
                except KeyError:
                        print("error : not found lastName in headers")
                        return JsonResponse({'err_msg': 'not found lastName in headers'})
                
                try:
                        user = request.data["guestIdToken"]
                except KeyError:
                        print("error : not found guestIdToken in body")
                        return JsonResponse({'err_msg': 'not found guestIdToken in body'})
                
                
                data = jwt.decode(token, options={'verify_signature': False})
                
                user_json = response.json()
                user_data = {
                        'platform'      : 'apple',
                        'id'            : user,
                        'sub'           : user_json['sub'],
                        'email'         : user_json['email'],
                        'first_name'    : first_name,
                        'last_name'     : last_name,
                        'full_name'     : last_name + ' ' + first_name,
                }
                user, msg = user_link(**user_data)
                
                if user:
                        return JsonResponse({'success': 1, 'msg': msg}, status=200)
                else:
                        return JsonResponse({'success': 0, 'msg': msg}, status=400)