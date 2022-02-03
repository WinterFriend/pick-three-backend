from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from django.utils.translation import gettext_lazy as _

from pick_restful.models import User, SocialPlatform, Goal, UserGoal
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(SocialPlatform)
class SocialAdmin(admin.ModelAdmin):
    actions = None
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

class UserGoalInline(admin.TabularInline):
    model = UserGoal
    fields = ('goal', 'select_date', 'input_date', 'diary', 'success', 'active')

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    actions = None
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
    ordering = ('-date_joined', )
    list_filter = ('social', 'date_joined', 'last_login')
    list_display = ('full_name', 'email', 'date_joined', 'last_login', 'social', 'id', 'sub', 'is_active')
    search_fields = ('full_name', 'id')
    readonly_fields = ('full_name', 'email', 'social', 'id', 'sub', 'password', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'date_birth',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    actions = None
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(UserGoal)
class UserGoalAdmin(admin.ModelAdmin):
    actions = None
    list_display_links = None
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_uuid(self, obj):
        return obj.user.id
    get_uuid.short_description = 'UUID'

    fieldsets = (
        (None, {'fields': ('user', 'goal', 'select_date', 'input_date')}),
        (None, {'fields': (
            'success',
            'active',
        )}),
    )
    list_filter = ('goal', 'select_date', 'success', 'active')
    list_display = ('user', 'get_uuid', 'goal', 'diary', 'select_date', 'input_date', 'success', 'active')
    search_fields = ('select_date', 'user__full_name', 'user__id')