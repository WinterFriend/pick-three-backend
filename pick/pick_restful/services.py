from typing import Tuple

from django.db import transaction
from django.core.management.utils import get_random_secret_key

from utils import get_now

from pick_restful.models import User, SocialPlatform
from django.utils import timezone

def user_create_superuser(email, password=None, **extra_fields) -> User:
    extra_fields = {
        **extra_fields,
        'is_staff': True,
        'is_superuser': True
    }

    user = user_create(email=email, social="google", password=password, **extra_fields)

    return user

def user_create(email, social, password=None, **extra_fields) -> User:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
        **extra_fields
    }

    user = User(email=email, social=SocialPlatform.objects.get(platform=social), **extra_fields)

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
def user_get_or_create(*, email: str, social: str, **extra_data) -> Tuple[User, bool]:
    user = User.objects.filter(email=email).first() # 이거 필터에서 소셜도 넣어야함 나중에 꼭!
    
    if user:
        user.last_login = timezone.localtime()
        user.save()
        return user, False

    return user_create(email=email, social=social, **extra_data), True