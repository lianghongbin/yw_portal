from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile
from apps.rbac.models import UserRole


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户档案'


class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline, UserRoleInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'department', 'position', 'is_staff', 'is_active', 'get_roles')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'department', 'is_employee', 'userrole__role')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'department', 'position')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('工作信息', {'fields': ('department', 'position', 'phone', 'employee_id')}),
        ('状态信息', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_employee', 'is_verified')}),
        ('权限', {'fields': ('groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'department', 'position'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'date_joined', 'last_login')
    
    def get_roles(self, obj):
        """显示用户角色"""
        roles = UserRole.objects.filter(user=obj)
        if roles:
            role_names = [role.role.name for role in roles]
            return format_html('<span class="badge bg-primary">{}</span>', ', '.join(role_names))
        return format_html('<span class="text-muted">无角色</span>')
    get_roles.short_description = '角色'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'emergency_contact', 'emergency_phone')
    list_filter = ('birth_date',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'emergency_contact')
    ordering = ('user',)
    
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('个人信息', {'fields': ('bio', 'birth_date', 'address')}),
        ('紧急联系人', {'fields': ('emergency_contact', 'emergency_phone')}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
