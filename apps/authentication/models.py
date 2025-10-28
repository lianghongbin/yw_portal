from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import BaseModel


class User(AbstractUser):
    """扩展用户模型"""
    # 基本信息
    avatar = models.ImageField(upload_to='avatars/', verbose_name='头像', blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name='电话', blank=True)
    
    # 工作信息
    department = models.CharField(max_length=100, verbose_name='部门', blank=True)
    position = models.CharField(max_length=100, verbose_name='职位', blank=True)
    employee_id = models.CharField(max_length=20, verbose_name='工号', blank=True)
    
    # 状态信息
    is_employee = models.BooleanField(default=True, verbose_name='是否员工')
    is_verified = models.BooleanField(default=False, verbose_name='是否验证')
    
    # 时间信息
    last_login_ip = models.GenericIPAddressField(verbose_name='最后登录IP', blank=True, null=True)
    last_login_location = models.CharField(max_length=100, verbose_name='最后登录位置', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'auth_user'

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or self.first_name or self.last_name})"

    @property
    def display_name(self):
        """显示名称"""
        return self.get_full_name() or self.username

    @property
    def is_online(self):
        """是否在线"""
        # 这里可以实现在线状态检查
        return True


class UserProfile(BaseModel):
    """用户档案"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')
    address = models.CharField(max_length=255, blank=True, verbose_name='地址')
    emergency_contact = models.CharField(max_length=100, blank=True, verbose_name='紧急联系人')
    emergency_phone = models.CharField(max_length=20, blank=True, verbose_name='紧急联系电话')

    class Meta:
        verbose_name = '用户档案'
        verbose_name_plural = '用户档案'

    def __str__(self):
        return f"{self.user.username} 的档案"
