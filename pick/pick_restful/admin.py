from django.contrib import admin
from .models import SocialPlatform, User

class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']

admin.site.register(SocialPlatform)
admin.site.register(User, UserAdmin)