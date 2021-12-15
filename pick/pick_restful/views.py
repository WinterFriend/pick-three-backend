from django.shortcuts import render

from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect
from .models import User, SocialPlatform

import requests

def index(request):
        return HttpResponse("연결성공")

class GoogleLoginView(View): 
        def get(self,request):
                token = request.headers["Authorization"]
                print('dd')
                print(token) ###########################################################################
                url = 'https://oauth2.googleapis.com/tokeninfo?id_token='
                response = requests.get(url+token)
                print("response: ", response)
                user = response.json()
                print("user : ", user) ###########################################################################

                if User.objects.filter(social_login_id = user['sub']).exists():
                        user_data = User.objects.get(social_login_id=user['sub'])
                        encoded_jwt = jwt.encode({'id': user["sub"]}, wef_key, algorithm='HS256')

                        return JsonResponse({
                                'access_token'  : encoded_jwt.decode('UTF-8'),
                                'user_name'     : user['name'],
                                'user_id'       : user_data.id
                        }, status = 200)
                else:
                        user_data = User(social_login_id = user['sub'],
                                name = user['name'],
                                social = SocialPlatform.objects.get(platform="google"),
                                email = user.get('email', "")
                                #email = user['email']
                        )
                        user_data.save()
                        encoded_jwt = jwt.encode({'id': user_data.id}, wef_key, algorithm='HS256')

                        return JsonResponse({
                                'user_id'       : user_data.id,
                                'user_name'     : user_data.username,
                                'access_token'  : encoded_jwt.decode('UTF-8')
                        }, status = 200)