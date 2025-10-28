"""
主 URL 配置文件
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 管理后台
    path('admin/', admin.site.urls),
    
    # 认证模块
    path('', include('apps.authentication.urls')),
    
    # 门户模块
    path('portal/', include('apps.portal.urls')),
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
