from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import date, time
from decimal import Decimal
from apps.portal.models import (
    DailyReport, DeliveryReport, WarehouseReport, 
    PickupReport, AirTransportReport, LinehaulReport, ChangeOrderChannel
)

User = get_user_model()


class DailyReportModelTest(TestCase):
    """日报模型测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.report = DailyReport.objects.create(
            report_date=date.today(),
            reporter=self.user,
            is_published=True,
            notes='测试日报'
        )
    
    def test_daily_report_creation(self):
        """测试日报创建"""
        self.assertEqual(self.report.report_date, date.today())
        self.assertEqual(self.report.reporter, self.user)
        self.assertTrue(self.report.is_published)
        self.assertEqual(self.report.notes, '测试日报')
    
    def test_daily_report_str(self):
        """测试日报字符串表示"""
        expected = f"LAX日报 - {date.today()}"
        self.assertEqual(str(self.report), expected)


class DeliveryReportModelTest(TestCase):
    """配送报告模型测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.daily_report = DailyReport.objects.create(
            report_date=date.today(),
            reporter=self.user,
            is_published=True
        )
        self.delivery_report = DeliveryReport.objects.create(
            daily_report=self.daily_report,
            city='LAX',
            cargo_volume=1000,
            box_count=50,
            open_time=time(8, 0),
            sorting_error_rate=Decimal('0.5'),
            sorting_error_count=5,
            delivery_rate_1=Decimal('95.0'),
            delivery_rate_2=Decimal('98.0'),
            delivery_rate_3=Decimal('99.0'),
            stranded_boxes=0,
            exception_notes=''
        )
    
    def test_delivery_report_creation(self):
        """测试配送报告创建"""
        self.assertEqual(self.delivery_report.city, 'LAX')
        self.assertEqual(self.delivery_report.cargo_volume, 1000)
        self.assertEqual(self.delivery_report.box_count, 50)
        self.assertEqual(self.delivery_report.sorting_error_rate, Decimal('0.5'))
    
    def test_delivery_report_str(self):
        """测试配送报告字符串表示"""
        expected = f"LAX配送报告 - {date.today()}"
        self.assertEqual(str(self.delivery_report), expected)


class WarehouseReportModelTest(TestCase):
    """仓内报告模型测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.daily_report = DailyReport.objects.create(
            report_date=date.today(),
            reporter=self.user,
            is_published=True
        )
        self.warehouse_report = WarehouseReport.objects.create(
            daily_report=self.daily_report,
            contractor_company='HR Solution',
            attendance_count=10,
            work_type='Regular Sorter',
            actual_hours=80,
            yesterday_cost=Decimal('1000.00'),
            cost_per_ticket=Decimal('0.16'),
            exception_notes=''
        )
    
    def test_warehouse_report_creation(self):
        """测试仓内报告创建"""
        self.assertEqual(self.warehouse_report.contractor_company, 'HR Solution')
        self.assertEqual(self.warehouse_report.attendance_count, 10)
        self.assertEqual(self.warehouse_report.work_type, 'Regular Sorter')
        self.assertEqual(self.warehouse_report.actual_hours, 80)


class PortalViewsTest(TestCase):
    """Portal视图测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        # 创建测试数据
        self.daily_report = DailyReport.objects.create(
            report_date=date.today(),
            reporter=self.user,
            is_published=True,
            notes='测试日报'
        )
        
        self.delivery_report = DeliveryReport.objects.create(
            daily_report=self.daily_report,
            city='LAX',
            cargo_volume=1000,
            box_count=50,
            open_time=time(8, 0),
            sorting_error_rate=Decimal('0.5'),
            sorting_error_count=5,
            delivery_rate_1=Decimal('95.0'),
            delivery_rate_2=Decimal('98.0'),
            delivery_rate_3=Decimal('99.0'),
            stranded_boxes=0,
            exception_notes=''
        )
    
    def test_dashboard_view(self):
        """测试仪表板视图"""
        response = self.client.get(reverse('portal:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'LAX日报关键指标')
    
    def test_daily_reports_view(self):
        """测试日报列表视图"""
        response = self.client.get(reverse('portal:daily_reports'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'LAX日报列表')
    
    def test_daily_report_detail_view(self):
        """测试日报详情视图"""
        response = self.client.get(reverse('portal:daily_report_detail', args=[self.daily_report.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'LAX日报详情')
    
    def test_delivery_module_view(self):
        """测试配送管理模块视图"""
        response = self.client.get(reverse('portal:delivery_module'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '配送管理模块')
    
    def test_warehouse_module_view(self):
        """测试仓内管理模块视图"""
        response = self.client.get(reverse('portal:warehouse_module'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '仓内管理模块')
    
    def test_pickup_module_view(self):
        """测试揽收管理模块视图"""
        response = self.client.get(reverse('portal:pickup_module'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '揽收管理模块')
    
    def test_airtransport_module_view(self):
        """测试空运管理模块视图"""
        response = self.client.get(reverse('portal:airtransport_module'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '空运管理模块')
    
    def test_linehaul_module_view(self):
        """测试干线管理模块视图"""
        response = self.client.get(reverse('portal:linehaul_module'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '干线管理模块')
    
    def test_change_order_module_view(self):
        """测试换单管理模块视图"""
        response = self.client.get(reverse('portal:change_order_module'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '换单管理模块')
    
    def test_dashboard_api_view(self):
        """测试仪表板API视图"""
        response = self.client.get(reverse('portal:dashboard_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = response.json()
        self.assertIn('labels', data)
        self.assertIn('cargo_volume', data)
        self.assertIn('box_count', data)
        self.assertIn('error_rate', data)
        self.assertIn('delivery_rate', data)


class PortalUrlsTest(TestCase):
    """Portal URL测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_url_patterns(self):
        """测试URL模式"""
        # 测试所有URL是否可访问
        urls = [
            'portal:dashboard',
            'portal:daily_reports',
            'portal:delivery_module',
            'portal:warehouse_module',
            'portal:pickup_module',
            'portal:airtransport_module',
            'portal:linehaul_module',
            'portal:change_order_module',
            'portal:dashboard_api',
        ]
        
        for url_name in urls:
            with self.subTest(url=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)


class PortalAdminTest(TestCase):
    """Portal Admin测试"""
    
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass123')
    
    def test_admin_access(self):
        """测试管理员访问"""
        response = self.client.get('/admin/portal/')
        self.assertEqual(response.status_code, 200)
    
    def test_daily_report_admin(self):
        """测试日报管理界面"""
        response = self.client.get('/admin/portal/dailyreport/')
        self.assertEqual(response.status_code, 200)
    
    def test_delivery_report_admin(self):
        """测试配送报告管理界面"""
        response = self.client.get('/admin/portal/deliveryreport/')
        self.assertEqual(response.status_code, 200)
    
    def test_warehouse_report_admin(self):
        """测试仓内报告管理界面"""
        response = self.client.get('/admin/portal/warehousereport/')
        self.assertEqual(response.status_code, 200)
