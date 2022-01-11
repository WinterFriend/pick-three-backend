from typing import Tuple
from django.db import transaction
from django.core.management.utils import get_random_secret_key
from rest_framework_simplejwt.tokens import RefreshToken
from pick_restful.models import User, SocialPlatform, UserGoal, Goal
from django.utils import timezone
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
def user_get_or_create(
    *, 
    sub: str, 
    social: str, 
    **extra_data
) -> Tuple[User, bool]:

    # 나중에 필터에 소셜도 필요할 수 있음
    user = User.objects.filter(sub=sub).first()
    if user:
        user.last_login = timezone.localtime()
        user.save()
        return user, False

    return user_create(sub=sub, social=social, **extra_data), True

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

    dictionary = {}
    dictionary['name'] = user.full_name
    dictionary['birth'] = user.date_birth
    dictionary['email'] = user.email
    return dictionary

@transaction.atomic
def set_user_profile(*, user: str, **data) -> None:
    user = User.objects.get(id=user)
    dictionary = {}
    if 'name' in data['updateColumn']:
        user.full_name = data['name']
    if 'email' in data['updateColumn']:
        user.email = data['email']
    if 'birth' in data['updateColumn']:
        user.date_birth = data['birth'] 
    user.save()