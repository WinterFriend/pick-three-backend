from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.management.utils import get_random_secret_key
from django.utils import timezone
import uuid


class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20, editable=False, null=False, blank=False)
    
    def __str__(self):
        return self.platform
    class Meta:
        db_table = "social_platform"


class User(AbstractUser):
    username        = None
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    date_birth      = models.DateField(default=timezone.localtime)
    sub             = models.CharField(max_length=64, db_index=True, null=False, blank=False) # 현재 sub는 unique=True 아님
    social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, default=1) # 무조건 social_platform에 1개이상 있어야함.

    USERNAME_FIELD  = 'id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.id)
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    @property
    def name(self):
        if not self.last_name:
            return self.first_name.capitalize()

        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'

class Goal(models.Model):
    name            = models.CharField(max_length=20, null=False, blank=False)
    description     = models.CharField(max_length=128, null=False, blank=False)
    icon            = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "goal"

class UserGoal(models.Model):
    goal_id         = models.ForeignKey(Goal, on_delete=models.CASCADE, max_length=20) # 무조건 goal에 1개이상 있어야함.
    select_date     = models.DateField(default=timezone.localtime)
    success         = models.BooleanField(default=0)
    input_date      = models.DateTimeField(default=datetime.now)
    diary           = models.TextField(max_length=1024)
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id.first_name
    class Meta:
        db_table = "user_goal"