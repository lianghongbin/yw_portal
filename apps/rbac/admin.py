from django.contrib import admin
from django.utils.html import format_html
from .models import Role, Resource, Permission, RolePermission, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'description', 'is_active')}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource_type', 'resource_code', 'parent', 'is_active')
    list_filter = ('resource_type', 'is_active', 'parent')
    search_fields = ('name', 'resource_code', 'description')
    ordering = ('resource_type', 'name')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'resource_type', 'resource_code')}),
        ('层级关系', {'fields': ('parent', 'sort_order')}),
        ('状态', {'fields': ('is_active',)}),
        ('时间信息', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'permission_code', 'permission_type', 'resource', 'is_active')
    list_filter = ('is_active', 'permission_type', 'resource__resource_type', 'resource')
    search_fields = ('name', 'permission_code', 'description')
    ordering = ('resource', 'permission_type', 'name')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'permission_code', 'permission_type')}),
        ('关联资源', {'fields': ('resource',)}),
        ('状态', {'fields': ('is_active',)}),
        ('时间信息', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'created_at')
    list_filter = ('role', 'permission__resource', 'created_at')
    search_fields = ('role__name', 'permission__name')
    ordering = ('role', 'permission')
    fieldsets = (
        (None, {'fields': ('role', 'permission')}),
        ('时间信息', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'role__name')
    ordering = ('user', 'role')
    fieldsets = (
        (None, {'fields': ('user', 'role')}),
        ('时间信息', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)
