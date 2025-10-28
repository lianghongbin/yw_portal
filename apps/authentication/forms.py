from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """自定义用户注册表单"""
    email = forms.EmailField(required=True, label='邮箱')
    first_name = forms.CharField(max_length=30, required=True, label='名字')
    last_name = forms.CharField(max_length=30, required=True, label='姓氏')
    department = forms.CharField(max_length=100, required=True, label='部门')
    position = forms.CharField(max_length=100, required=True, label='职位')
    phone = forms.CharField(max_length=20, required=False, label='电话')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'department', 'position', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CustomAuthenticationForm(AuthenticationForm):
    """自定义登录表单"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': '用户名'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': '密码'})
