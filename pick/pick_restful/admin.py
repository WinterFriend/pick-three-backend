from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from django.utils.translation import gettext_lazy as _

from pick_restful.models import User, SocialPlatform, Goal, UserGoal
from django.contrib.auth.models import Group

admin.site.unregister(Group)

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

class UserGoalInline(admin.TabularInline):
    model = UserGoal

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    readonly_fields=('id', 'email', 'social')

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

    inlines = [
        UserGoalInline,
    ] 

    fieldsets = (
        (_('Personal info'), {'fields': ('full_name', 'email', 'social', 'id', 'sub', 'password', )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            # 'groups',
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'date_birth')}),
    )
    ordering = ('id', )
    list_display = ('full_name', 'id', 'social', 'sub', 'email')
    search_fields = ('full_name', 'id')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    #actions = None
    #list_display_links = None
    
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    '''
    def has_change_permission(self, request, obj=None):
        return False'''

@admin.register(UserGoal)
class UserGoalAdmin(admin.ModelAdmin):
    #actions = None
    #list_display_links = None
    '''
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False'''
    
    fieldsets = (
        (None, {'fields': ('user', 'goal', 'select_date', 'input_date', 'diary')}),
        (None, {'fields': (
            'success',
            'active',
        )}),
    )
    list_display = ('user', 'goal', 'select_date', 'input_date', 'diary', 'success', 'active')
    search_fields = ('select_date', 'diary')