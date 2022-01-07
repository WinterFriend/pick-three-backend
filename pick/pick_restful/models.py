from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.management.utils import get_random_secret_key
from django.utils import timezone
import uuid


class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20, editable=False, null=False, blank=False, verbose_name="가입 경로")
    
    def __str__(self):
        return self.platform

    class Meta:
        db_table = "social_platform"
        verbose_name = '가입 경로'
        verbose_name_plural = '가입 경로'


class User(AbstractUser):
    username        = None
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True, verbose_name="UUID")
    date_birth      = models.DateField(default=timezone.localtime, verbose_name="생일")
    sub             = models.CharField(max_length=64, db_index=True, null=False, blank=False, verbose_name="SUB") # 현재 sub는 unique=True 아님
    social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, default=1, verbose_name="가입 경로") # 무조건 social_platform에 1개이상 있어야함.
    full_name       = models.CharField(max_length=64, null=False, blank=False, default='', verbose_name="이름")

    USERNAME_FIELD  = 'id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.full_name)

    class Meta:
        db_table = "user"
        swappable = 'AUTH_USER_MODEL'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'

    '''
    @property
    def name(self):
        if not self.last_name:
            return self.first_name.capitalize()

        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'
    '''

class Goal(models.Model):
    name            = models.CharField(max_length=20, null=False, blank=False, default="", verbose_name="이름")
    description     = models.CharField(max_length=128, null=False, blank=False, default="", verbose_name="설명")
    active_icon     = models.CharField(max_length=128, null=False, blank=False, default="", verbose_name="활성 아이콘")
    inactive_icon   = models.CharField(max_length=128, null=False, blank=False, default="", verbose_name="비활성 아이콘")
    main_color      = models.CharField(max_length=9, null=False, blank=False, default="", verbose_name="메인 색상")
    sub_color       = models.CharField(max_length=9, null=False, blank=False, default="", verbose_name="서브 색상")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "goal"
        verbose_name = '목표 분류'
        verbose_name_plural = '목표 분류'

class UserGoal(models.Model):
    goal            = models.ForeignKey(Goal, on_delete=models.CASCADE, max_length=20, verbose_name="목표") # 무조건 goal에 1개이상 있어야함.
    select_date     = models.DateField(default=timezone.localtime, verbose_name="선택 날짜")
    input_date      = models.DateTimeField(default=datetime.now, verbose_name="수정 시간")
    diary           = models.TextField(max_length=200, verbose_name="일기", default='')
    user            = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")
    success         = models.BooleanField(default=0, verbose_name="성공")
    active          = models.BooleanField(default=0, verbose_name="활성화")

    def __str__(self):
        return self.user.first_name
    
    class Meta:
        db_table = "user_goal"
        verbose_name = '사용자 목표'
        verbose_name_plural = '사용자 목표'
        ordering = ['-select_date', 'goal']