from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.management.utils import get_random_secret_key
from django.utils import timezone

'''
class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20, default=0)

    class Meta:
        db_table = "social_platform"
'''

class User(AbstractUser):
    username        = None
    date_birth      = models.DateField(default=timezone.localtime)
    email           = models.EmailField(unique=True, db_index=True)
    secret_key      = models.CharField(max_length=255, default=get_random_secret_key)

    #name            = models.CharField(max_length=254)
    #social_login_id = models.CharField(max_length=50, blank=True)
    #social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, blank=True, default=1)
    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    @property
    def name(self):
        if not self.last_name:
            return self.first_name.capitalize()

        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'
        