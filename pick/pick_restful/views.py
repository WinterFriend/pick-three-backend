from django.shortcuts import render

from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect
from .models import User

# Create your views here.

def index(request):
        return redirect('https://wintyio.github.io/pick-three-frontend-intro-web/')

class GoogleLoginView(View): 
        def get(self,request):
                token = request.headers["Auth"]
                url = 'https://oauth2.googleapis.com/tokeninfo?id_token='
                response = requests.get(url+token)
                user = response.json()

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
                                social = SocialPlatform.objects.get(platform ="google"),
                                email = user.get('email', None)
                        )
                        user_data.save()
                        encoded_jwt = jwt.encode({'id': user_data.id}, wef_key, algorithm='HS256')

                        return JsonResponse({
                                'user_id'       : user_data.id,
                                'user_name'     : user_data.username,
                                'access_token'  : encoded_jwt.decode('UTF-8')
                        }, status = 200)
