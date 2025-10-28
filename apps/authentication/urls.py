from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'authentication'

def redirect_to_portal(request):
    """重定向到门户首页"""
    return redirect('/portal/')

urlpatterns = [
    path('', redirect_to_portal, name='index'),  # 根路径重定向
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
