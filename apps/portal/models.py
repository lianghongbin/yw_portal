from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Announcement(BaseModel):
    """公告模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    is_published = models.BooleanField(default=True, verbose_name='是否发布')
    priority = models.IntegerField(default=0, verbose_name='优先级')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.title


# ==================== LAX日报相关模型 ====================

class DailyReport(BaseModel):
    """日报主表"""
    report_date = models.DateField(verbose_name='报告日期')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='报告人')
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    notes = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '日报'
        verbose_name_plural = '日报'
        ordering = ['-report_date']
        unique_together = ['report_date']

    def __str__(self):
        return f"LAX日报 - {self.report_date}"


class DeliveryReport(BaseModel):
    """配送报告 - 基于LAX日报实际数据结构"""
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='delivery_reports', verbose_name='日报')
    city = models.CharField(max_length=10, verbose_name='配送城市')
    
    # 基础数据
    cargo_volume = models.PositiveIntegerField(verbose_name='货量')
    box_count = models.PositiveIntegerField(verbose_name='分箱数')
    open_time = models.TimeField(verbose_name='开放时间')
    
    # 现场情况
    site_situation = models.TextField(blank=True, verbose_name='现场情况')
    
    # 配送时效（3天达成率）
    delivery_rate_day1 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='第1天达成率(%)')
    delivery_rate_day2 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='第2天达成率(%)')
    delivery_rate_day3 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='第3天达成率(%)')
    
    # 包裹移除数据
    removed_packages = models.PositiveIntegerField(verbose_name='包裹移除数')
    removal_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='移除率(%)')
    
    # 异常说明
    exception_notes = models.TextField(blank=True, verbose_name='异常说明')

    class Meta:
        verbose_name = '配送报告'
        verbose_name_plural = '配送报告'
        ordering = ['city']

    def __str__(self):
        return f"{self.city}配送报告 - {self.daily_report.report_date}"


class WarehouseReport(BaseModel):
    """仓内报告"""
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='warehouse_reports', verbose_name='日报')
    contractor_company = models.CharField(max_length=100, verbose_name='劳务公司')
    attendance_count = models.PositiveIntegerField(verbose_name='今日到岗人数')
    work_type = models.CharField(max_length=50, verbose_name='工种')
    actual_hours = models.PositiveIntegerField(verbose_name='实际工时')
    yesterday_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='昨日成本')
    cost_per_ticket = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='单票成本')
    exception_notes = models.TextField(blank=True, verbose_name='异常说明')

    class Meta:
        verbose_name = '仓内报告'
        verbose_name_plural = '仓内报告'
        ordering = ['contractor_company']

    def __str__(self):
        return f"{self.contractor_company}仓内报告 - {self.daily_report.report_date}"


class PickupReport(BaseModel):
    """揽收报告"""
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='pickup_reports', verbose_name='日报')
    pickup_area = models.CharField(max_length=20, verbose_name='揽收区域')
    pickup_situation = models.TextField(verbose_name='揽收情况')
    return_count = models.PositiveIntegerField(verbose_name='回库件数')
    exception_notes = models.TextField(blank=True, verbose_name='异常说明')

    class Meta:
        verbose_name = '揽收报告'
        verbose_name_plural = '揽收报告'
        ordering = ['pickup_area']

    def __str__(self):
        return f"{self.pickup_area}揽收报告 - {self.daily_report.report_date}"


class AirTransportReport(BaseModel):
    """空运报告"""
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='air_transport_reports', verbose_name='日报')
    flight_city = models.CharField(max_length=10, verbose_name='飞航城市')
    pickup_date = models.DateField(verbose_name='揽收日')
    cargo_out_time = models.TimeField(verbose_name='货物出仓时间')
    box_count = models.PositiveIntegerField(verbose_name='箱数')

    class Meta:
        verbose_name = '空运报告'
        verbose_name_plural = '空运报告'
        ordering = ['flight_city']

    def __str__(self):
        return f"{self.flight_city}空运报告 - {self.daily_report.report_date}"


class LinehaulReport(BaseModel):
    """干线报告"""
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='linehaul_reports', verbose_name='日报')
    supplier = models.CharField(max_length=100, verbose_name='干线供应商')
    transport_type = models.CharField(max_length=50, verbose_name='发运类型')
    vehicle_type_count = models.PositiveIntegerField(verbose_name='车型及次数')
    billing_logic = models.CharField(max_length=50, verbose_name='计费逻辑')
    exception_notes = models.TextField(blank=True, verbose_name='异常说明')

    class Meta:
        verbose_name = '干线报告'
        verbose_name_plural = '干线报告'
        ordering = ['supplier']

    def __str__(self):
        return f"{self.supplier}干线报告 - {self.daily_report.report_date}"


class ChangeOrderChannel(BaseModel):
    """换单渠道"""
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='change_order_channels', verbose_name='日报')
    channel_name = models.CharField(max_length=100, verbose_name='换单渠道')
    change_order_count = models.PositiveIntegerField(verbose_name='换单量')
    exception_notes = models.TextField(blank=True, verbose_name='异常说明')

    class Meta:
        verbose_name = '换单渠道'
        verbose_name_plural = '换单渠道'
        ordering = ['channel_name']

    def __str__(self):
        return f"{self.channel_name}换单渠道 - {self.daily_report.report_date}"


class SortingMachineReport(BaseModel):
    """分拣机报告"""
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='sorting_machine_reports', verbose_name='日报')
    machine_name = models.CharField(max_length=50, verbose_name='分拣机名称')
    machine_type = models.CharField(max_length=30, verbose_name='分拣机类型')
    throughput = models.PositiveIntegerField(verbose_name='处理量(件/小时)')
    error_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='错误率(%)')
    downtime_hours = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='停机时间(小时)')
    maintenance_status = models.CharField(max_length=20, verbose_name='维护状态')
    exception_notes = models.TextField(blank=True, verbose_name='异常说明')

    class Meta:
        verbose_name = '分拣机报告'
        verbose_name_plural = '分拣机报告'
        ordering = ['machine_name']

    def __str__(self):
        return f"{self.machine_name}分拣机报告 - {self.daily_report.report_date}"


class EquipmentReport(BaseModel):
    """设备报告"""
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='equipment_reports', verbose_name='日报')
    equipment_name = models.CharField(max_length=50, verbose_name='设备名称')
    equipment_type = models.CharField(max_length=30, verbose_name='设备类型')
    status = models.CharField(max_length=20, verbose_name='运行状态')
    utilization_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='利用率(%)')
    maintenance_hours = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='维护时间(小时)')
    exception_notes = models.TextField(blank=True, verbose_name='异常说明')

    class Meta:
        verbose_name = '设备报告'
        verbose_name_plural = '设备报告'
        ordering = ['equipment_name']

    def __str__(self):
        return f"{self.equipment_name}设备报告 - {self.daily_report.report_date}"


class QualityReport(BaseModel):
    """质量报告"""
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='quality_reports', verbose_name='日报')
    quality_type = models.CharField(max_length=30, verbose_name='质量类型')
    total_count = models.PositiveIntegerField(verbose_name='总件数')
    error_count = models.PositiveIntegerField(verbose_name='错误件数')
    error_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='错误率(%)')
    improvement_measures = models.TextField(blank=True, verbose_name='改进措施')
    exception_notes = models.TextField(blank=True, verbose_name='异常说明')

    class Meta:
        verbose_name = '质量报告'
        verbose_name_plural = '质量报告'
        ordering = ['quality_type']

    def __str__(self):
        return f"{self.quality_type}质量报告 - {self.daily_report.report_date}"


class CostReport(BaseModel):
    """成本报告"""
    daily_report = models.ForeignKey(DailyReport, on_delete=models.CASCADE, related_name='cost_reports', verbose_name='日报')
    cost_category = models.CharField(max_length=30, verbose_name='成本类别')
    planned_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='计划成本')
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实际成本')
    variance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='差异')
    variance_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='差异率(%)')
    exception_notes = models.TextField(blank=True, verbose_name='异常说明')

    class Meta:
        verbose_name = '成本报告'
        verbose_name_plural = '成本报告'
        ordering = ['cost_category']

    def __str__(self):
        return f"{self.cost_category}成本报告 - {self.daily_report.report_date}"


class Department(BaseModel):
    """部门模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='部门名称')
    description = models.TextField(blank=True, verbose_name='部门描述')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                             verbose_name='部门经理', related_name='managed_departments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              verbose_name='上级部门')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'
        ordering = ['name']

    def __str__(self):
        return self.name


class Document(BaseModel):
    """文档模型"""
    DOCUMENT_TYPES = (
        ('policy', '政策文件'),
        ('procedure', '流程文件'),
        ('form', '表单'),
        ('template', '模板'),
        ('other', '其他'),
    )
    
    title = models.CharField(max_length=200, verbose_name='标题')
    description = models.TextField(blank=True, verbose_name='描述')
    file = models.FileField(upload_to='documents/', verbose_name='文件')
    category = models.CharField(max_length=50, verbose_name='分类')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, 
                                    default='other', verbose_name='文档类型')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='上传者')
    is_public = models.BooleanField(default=True, verbose_name='是否公开')
    download_count = models.PositiveIntegerField(default=0, verbose_name='下载次数')

    class Meta:
        verbose_name = '文档'
        verbose_name_plural = '文档'
        ordering = ['-created_at']

    def __str__(self):
        return self.title