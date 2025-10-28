from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class CustomLoginView(LoginView):
    """自定义登录视图"""
    form_class = CustomAuthenticationForm
    template_name = 'authentication/login.html'
    
    def get_success_url(self):
        return reverse_lazy('portal:dashboard')


class SignUpView(CreateView):
    """用户注册视图"""
    form_class = CustomUserCreationForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('authentication:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '注册成功！请登录。')
        return response


@login_required
def profile_view(request):
    """用户个人资料页面"""
    return render(request, 'authentication/profile.html')


@login_required
def logout_view(request):
    """登出视图"""
    logout(request)
    messages.success(request, '您已成功登出。')
    return redirect('authentication:login')
