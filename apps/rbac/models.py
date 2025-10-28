from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel

User = get_user_model()


class Role(BaseModel):
    """角色模型"""
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    description = models.TextField(blank=True, verbose_name='角色描述')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'
        ordering = ['name']

    def __str__(self):
        return self.name


class Resource(BaseModel):
    """资源模型"""
    RESOURCE_TYPES = (
        ('menu', '菜单'),
        ('api', 'API接口'),
        ('data', '数据'),
        ('function', '功能'),
    )
    
    name = models.CharField(max_length=50, unique=True, verbose_name='资源名称')
    description = models.TextField(blank=True, verbose_name='资源描述')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, verbose_name='资源类型')
    resource_code = models.CharField(max_length=100, unique=True, verbose_name='资源编码')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父资源')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    sort_order = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        verbose_name = '资源'
        verbose_name_plural = '资源'
        ordering = ['resource_type', 'sort_order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"


class Permission(BaseModel):
    """权限模型"""
    PERMISSION_TYPES = (
        ('read', '查看'),
        ('create', '创建'),
        ('update', '修改'),
        ('delete', '删除'),
        ('execute', '执行'),
    )
    
    name = models.CharField(max_length=50, verbose_name='权限名称')
    description = models.TextField(blank=True, verbose_name='权限描述')
    permission_code = models.CharField(max_length=100, unique=True, verbose_name='权限编码')
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPES, verbose_name='权限类型')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name='所属资源')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = '权限'
        ordering = ['resource', 'permission_type']

    def __str__(self):
        return f"{self.name} ({self.resource.name})"


class RolePermission(BaseModel):
    """角色权限关联模型"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')

    class Meta:
        verbose_name = '角色权限'
        verbose_name_plural = '角色权限'
        unique_together = ['role', 'permission']
        ordering = ['role', 'permission']

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


class UserRole(BaseModel):
    """用户角色关联模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')

    class Meta:
        verbose_name = '用户角色'
        verbose_name_plural = '用户角色'
        unique_together = ['user', 'role']
        ordering = ['user', 'role']

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
