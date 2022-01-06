from typing import Tuple

from django.db import transaction
from django.core.management.utils import get_random_secret_key

from utils import get_now

from pick_restful.models import User, SocialPlatform, UserGoal, Goal
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

def user_create_superuser(id, password=None, **extra_fields) -> User:
    extra_fields = {
        **extra_fields,
        'is_staff': True,
        'is_superuser': True,
        'id': id
    }

    user = user_create('0', social="google", password=password, **extra_fields)

    return user

def user_create(sub, social, password=None, **extra_fields) -> User:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
        **extra_fields
    }

    user = User(sub=sub, social=SocialPlatform.objects.get(platform=social), **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user

def user_record_login(*, user: User) -> User:
    user.last_login = get_now()
    user.save()

    return user

@transaction.atomic
def user_change_secret_key(*, user: User) -> User:
    user.secret_key = get_random_secret_key()
    user.full_clean()
    user.save()

    return user

@transaction.atomic
def user_get_or_create(*, sub: str, social: str, **extra_data) -> Tuple[User, bool]:
    user = User.objects.filter(sub=sub).first() # 이거 필터에서 소셜도 넣어야함 나중에 꼭!
    
    if user:
        user.last_login = timezone.localtime()
        user.save()
        return user, False

    return user_create(sub=sub, social=social, **extra_data), True

def jwt_login(user: User):
    refresh = RefreshToken.for_user(user)

    print(  'refresh_token : ',     str(refresh))
    print(  'access_token : ',      str(refresh.access_token))

    return {
        'refresh':      str(refresh),
        'access':       str(refresh.access_token),
    }

@transaction.atomic
def user_goal_detail_set(date: str, user_id: str, userGoalList: list):
    user_goal = UserGoal.objects.filter(select_date=date, user_id=user_id)
    user_goal.update(active=0)
    for obj in userGoalList:
        UserGoal.objects.update_or_create(select_date=date, user=User.objects.get(id=user_id), goal=Goal.objects.get(id=int(obj['goalId'])), 
            defaults={'active':1, 'diary':obj['diary'], 'success':obj['success']})