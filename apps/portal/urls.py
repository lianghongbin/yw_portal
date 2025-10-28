from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    # 用户前台页面
    path('', views.dashboard_view, name='dashboard'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('announcements/<int:pk>/', views.announcement_detail_view, name='announcement_detail'),
    path('documents/', views.documents_view, name='documents'),
    path('departments/', views.departments_view, name='departments'),
    
    # LAX日报相关页面
    path('daily-reports/', views.daily_reports_view, name='daily_reports'),
    path('daily-reports/<int:pk>/', views.daily_report_detail_view, name='daily_report_detail'),
    
    # 各业务模块页面
    path('delivery/', views.delivery_module_view, name='delivery_module'),
    path('warehouse/', views.warehouse_module_view, name='warehouse_module'),
    path('pickup/', views.pickup_module_view, name='pickup_module'),
    path('airtransport/', views.airtransport_module_view, name='airtransport_module'),
    path('linehaul/', views.linehaul_module_view, name='linehaul_module'),
    path('change-order/', views.change_order_module_view, name='change_order_module'),
    
    # 设备管理模块
    path('sorting-machine/', views.sorting_machine_module_view, name='sorting_machine_module'),
    path('equipment-maintenance/', views.equipment_maintenance_module_view, name='equipment_maintenance_module'),
    
    # 质量管理模块
    path('quality-monitoring/', views.quality_monitoring_module_view, name='quality_monitoring_module'),
    path('exception-handling/', views.exception_handling_module_view, name='exception_handling_module'),
    
    # 成本管理模块
    path('cost-analysis/', views.cost_analysis_module_view, name='cost_analysis_module'),
    
    # API接口
    path('api/dashboard/', views.dashboard_api_view, name='dashboard_api'),
]
