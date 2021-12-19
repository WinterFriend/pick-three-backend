from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from django.utils.translation import gettext_lazy as _

from pick_restful.models import User, SocialPlatform

@admin.register(SocialPlatform)
class SocialAdmin(admin.ModelAdmin):
    #actions = None
    #list_display_links = None
    
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    readonly_fields=('id', 'email', 'social')

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    
    fieldsets = (
        (None, {'fields': ('first_name', 'id', 'sub', 'email', 'social', 'password', )}),
        (_('Personal info'), {'fields': ('first_name',)}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'date_birth')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('id', )
    list_display = ('first_name', 'id', 'social', 'is_staff')
    search_fields = ('first_name', 'id')