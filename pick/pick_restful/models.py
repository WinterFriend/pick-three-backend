from django.db import models

class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20, default=0)

    class Meta:
        db_table = "social_platform"

class User(models.Model):
    last_login      = models.DateTimeField('date published')
    date_joined     = models.DateTimeField('date published', default=datetime.datetime.now)
    date_birth      = models.DateField()
    email           = models.CharField(max_length=254)
    username        = models.CharField(max_length=254)
    social          = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, blank=True, default=1)
    social_login_id = models.CharField(max_length=50, blank=True)