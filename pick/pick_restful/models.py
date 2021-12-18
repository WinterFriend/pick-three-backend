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
    id              = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name="uuid") #
    date_birth      = models.DateField(default=timezone.localtime)
    secret_key      = models.CharField(max_length=255, default=get_random_secret_key)
    social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, default=1) # 무조건 social_platform에 1개이상 있어야함.
    email           = models.EmailField(unique=True, db_index=True)
    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    @property
    def name(self):
        if not self.last_name:
            return self.first_name.capitalize()

        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'
        