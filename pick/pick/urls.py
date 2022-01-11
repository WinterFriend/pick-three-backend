"""pick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pick_restful import apis
from pick_restful.apis import GoogleLoginView, A, InfoGoalList, UserGoalDetailGet, UserGoalDetailSet, UserProfile

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', apis.index),
    path('login/google/',GoogleLoginView.as_view()),

    path('a/',A.as_view()),
    path('a',A.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pari'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('info/goal/list', InfoGoalList.as_view(), name='info_goal_list'),
    path('user/goal/detail/get', UserGoalDetailGet.as_view(), name='user_goal_detail_get'),
    path('user/goal/detail/set', UserGoalDetailSet.as_view(), name='user_goal_detail_set'),

    path('user/profile', UserProfile.as_view(), name='user_profile'),
]