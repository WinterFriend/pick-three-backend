from typing import Tuple
from django.db import transaction
from django.core.management.utils import get_random_secret_key
from rest_framework_simplejwt.tokens import RefreshToken
from pick_restful.models import User, SocialPlatform, UserGoal, Goal
from datetime import datetime
from utils import get_now

def user_create_superuser(id, password=None, **extra_fields) -> User:
    extra_fields = {
        **extra_fields,
        'is_staff': True,
        'is_superuser': True,
        'id': id
    }

    user = user_create('0', social="google",
                        password=password, **extra_fields)

    return user

def user_create(
    sub: str, 
    social: str, 
    password: str = None, 
    **extra_fields
) -> User:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
        **extra_fields
    }

    user = User(sub=sub,
                social=SocialPlatform.objects.get(platform=social), 
                **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user

def guest_create() -> User:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
    }

    user = User(sub=0,
                social=SocialPlatform.objects.get(platform="guest"),
                full_name='게스트',
                **extra_fields)
    user.set_unusable_password()

    user.full_clean()
    user.save()

    return user

def user_record_login(*, user: User) -> User:
    user.last_login = get_now()
    user.save()

    return user

def user_change_secret_key(*, user: User) -> User:
    user.secret_key = get_random_secret_key()
    user.full_clean()
    user.save()

    return user

def user_get_or_create(
    *,
    sub: str,
    social: str,
    **extra_data
) -> Tuple[User, bool]: # bool : 생성했으면 true 아니면 false

    # 나중에 필터에 소셜도 필요할 수 있음
    user = User.objects.filter(sub=sub).first()
    if user:
        user.last_login = datetime.now()
        user.save()
        return user, False

    return user_create(sub=sub, social=social, **extra_data), True



def user_link(
    *,
    platform: str,
    id: str,
    sub: str,
    email: str,
    first_name: str,
    last_name: str,
    full_name: str,
) -> Tuple[User, bool]: # bool : 생성했으면 true 아니면 false
    try:
        user = User.objects.filter(id=id).first()
    except:
        return None, "형식이 올바르지 않습니다.\n지속적인 문제 발생 시, 문의하기를 이용해주세요."
    
    if user:
        if str(user.social) == "guest":
            f = User.objects.filter(sub=sub).first()
            if f:
                return None, "본 계정은 이미 가입된 상태입니다.\n지속적인 문제 발생 시, 문의하기를 이용해주세요."
            else:
                user.sub        = sub
                user.social     = SocialPlatform.objects.get(platform=platform)
                user.email      = email
                # user.first_name = first_name
                # user.last_name  = last_name
                # user.full_name  = full_name
                user.date_birth = datetime.now()
                user.last_login = datetime.now()
                user.save()
                return user, "성공"
        else:
            return None, "게스트 계정이 아닙니다.\n지속적인 문제 발생 시, 문의하기를 이용해주세요."

    return None, "계정을 찾을 수 없습니다.\n지속적인 문제 발생 시, 문의하기를 이용해주세요."



def guest_get(user: str) -> Tuple[User, str]:
    try:
        user = User.objects.filter(id=user).first()
    except:
        return None, "Format not possible"
    
    if user:
        if str(user.social) == "guest":
            user.last_login = datetime.now()
            user.save()
            return user, "success"
        else:
            return None, "User is not guest"
    
    return None, "User not found"

def jwt_login(user: User):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':  str(refresh),
        'access':   str(refresh.access_token),
    }

@transaction.atomic
def user_goal_detail_set(
    date: str, 
    user_id: str, 
    userGoalList: list, 
    updateColumn: list
) -> None:
    user_goal = UserGoal.objects.filter(select_date=date, user_id=user_id)
    user_goal.update(active=0)
    for obj in userGoalList:
        defaults = {column : obj[column] for column in updateColumn}
        defaults['active'] = 1
        UserGoal.objects.update_or_create(select_date=date, user=User.objects.get(id=user_id), 
            goal=Goal.objects.get(id=int(obj['goalId'])), defaults=defaults)


def get_user_profile(user: str) -> dict:
    user = User.objects.get(id=user)

    dictionary = {'profile':{}}
    dictionary['profile']['name'] = user.full_name
    dictionary['profile']['birth'] = user.date_birth
    dictionary['profile']['social'] = user.social.platform
    dictionary['profile']['email'] = user.email
    return dictionary

def set_user_profile(*, user: str, **data) -> bool:
    user = User.objects.get(id=user)
    try:
        if 'name' in data['updateColumn']:
            user.full_name = data['profile']['name']
        # if 'email' in data['updateColumn']:
        #     user.email = data['profile']['email']
        if 'birth' in data['updateColumn']:
            user.date_birth = data['profile']['birth']
    except:
        return False
    user.save()
    return True
    
def delete_user(*, user: str) -> None:
    user = User.objects.get(id=user)
    user.is_active = 0
    user.sub = 0
    user.save()
    
def delete_user_undo(*, user: str) -> None:
    user = User.objects.get(id=user)
    user.is_active = 1
    user.save()