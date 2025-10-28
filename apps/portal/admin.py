from django.contrib import admin
from .models import (
    Announcement, Department, Document,
    DailyReport, DeliveryReport, WarehouseReport, 
    PickupReport, AirTransportReport, LinehaulReport, ChangeOrderChannel,
    SortingMachineReport, EquipmentReport, QualityReport, CostReport
)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'priority', 'created_at')
    list_filter = ('is_published', 'priority', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username', 'author__first_name')
    ordering = ('-priority', '-created_at')
    
    fieldsets = (
        (None, {'fields': ('title', 'content')}),
        ('发布设置', {'fields': ('author', 'is_published', 'priority')}),
        ('时间设置', {'fields': ('start_date', 'end_date')}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'manager')
    search_fields = ('name', 'description', 'manager__username', 'manager__first_name')
    ordering = ('name',)
    
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('管理设置', {'fields': ('manager', 'parent')}),
        ('状态', {'fields': ('is_active',)}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'document_type', 'uploaded_by', 'is_public', 'download_count', 'created_at')
    list_filter = ('is_public', 'document_type', 'category', 'created_at', 'uploaded_by')
    search_fields = ('title', 'description', 'uploaded_by__username', 'uploaded_by__first_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('title', 'description', 'file')}),
        ('分类设置', {'fields': ('category', 'document_type')}),
        ('权限设置', {'fields': ('uploaded_by', 'is_public')}),
        ('统计信息', {'fields': ('download_count',)}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'download_count')


# ==================== LAX日报相关Admin配置 ====================

class DeliveryReportInline(admin.TabularInline):
    model = DeliveryReport
    extra = 0
    fields = ('city', 'cargo_volume', 'box_count', 'open_time', 'delivery_rate_day1', 'removed_packages')


class WarehouseReportInline(admin.TabularInline):
    model = WarehouseReport
    extra = 0
    fields = ('contractor_company', 'attendance_count', 'work_type', 'actual_hours', 'yesterday_cost')


class PickupReportInline(admin.TabularInline):
    model = PickupReport
    extra = 0
    fields = ('pickup_area', 'pickup_situation', 'return_count')


class AirTransportReportInline(admin.TabularInline):
    model = AirTransportReport
    extra = 0
    fields = ('flight_city', 'pickup_date', 'cargo_out_time', 'box_count')


class LinehaulReportInline(admin.TabularInline):
    model = LinehaulReport
    extra = 0
    fields = ('supplier', 'transport_type', 'vehicle_type_count', 'billing_logic')


class ChangeOrderChannelInline(admin.TabularInline):
    model = ChangeOrderChannel
    extra = 0
    fields = ('channel_name', 'change_order_count')


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'reporter', 'is_published', 'created_at')
    list_filter = ('is_published', 'report_date', 'reporter', 'created_at')
    search_fields = ('report_date', 'reporter__username', 'notes')
    ordering = ('-report_date',)
    date_hierarchy = 'report_date'
    
    fieldsets = (
        (None, {'fields': ('report_date', 'reporter', 'is_published')}),
        ('备注', {'fields': ('notes',)}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    inlines = [
        DeliveryReportInline,
        WarehouseReportInline,
        PickupReportInline,
        AirTransportReportInline,
        LinehaulReportInline,
        ChangeOrderChannelInline,
    ]


@admin.register(DeliveryReport)
class DeliveryReportAdmin(admin.ModelAdmin):
    list_display = ('daily_report', 'city', 'cargo_volume', 'box_count', 'delivery_rate_day1', 'removed_packages')
    list_filter = ('city', 'daily_report__report_date', 'daily_report__reporter')
    search_fields = ('city', 'daily_report__report_date', 'exception_notes')
    ordering = ('daily_report__report_date', 'city')
    
    fieldsets = (
        (None, {'fields': ('daily_report', 'city')}),
        ('货量信息', {'fields': ('cargo_volume', 'box_count', 'open_time')}),
        ('现场情况', {'fields': ('site_situation',)}),
        ('配送时效', {'fields': ('delivery_rate_day1', 'delivery_rate_day2', 'delivery_rate_day3')}),
        ('包裹移除', {'fields': ('removed_packages', 'removal_rate')}),
        ('异常说明', {'fields': ('exception_notes',)}),
    )


@admin.register(WarehouseReport)
class WarehouseReportAdmin(admin.ModelAdmin):
    list_display = ('daily_report', 'contractor_company', 'attendance_count', 'actual_hours', 'yesterday_cost')
    list_filter = ('contractor_company', 'work_type', 'daily_report__report_date')
    search_fields = ('contractor_company', 'work_type', 'daily_report__report_date')
    ordering = ('daily_report__report_date', 'contractor_company')
    
    fieldsets = (
        (None, {'fields': ('daily_report', 'contractor_company')}),
        ('人员信息', {'fields': ('attendance_count', 'work_type', 'actual_hours')}),
        ('成本信息', {'fields': ('yesterday_cost', 'cost_per_ticket')}),
        ('异常说明', {'fields': ('exception_notes',)}),
    )


@admin.register(PickupReport)
class PickupReportAdmin(admin.ModelAdmin):
    list_display = ('daily_report', 'pickup_area', 'return_count')
    list_filter = ('pickup_area', 'daily_report__report_date')
    search_fields = ('pickup_area', 'pickup_situation', 'daily_report__report_date')
    ordering = ('daily_report__report_date', 'pickup_area')
    
    fieldsets = (
        (None, {'fields': ('daily_report', 'pickup_area')}),
        ('揽收信息', {'fields': ('pickup_situation', 'return_count')}),
        ('异常说明', {'fields': ('exception_notes',)}),
    )


@admin.register(AirTransportReport)
class AirTransportReportAdmin(admin.ModelAdmin):
    list_display = ('daily_report', 'flight_city', 'pickup_date', 'cargo_out_time', 'box_count')
    list_filter = ('flight_city', 'pickup_date', 'daily_report__report_date')
    search_fields = ('flight_city', 'daily_report__report_date')
    ordering = ('daily_report__report_date', 'flight_city')
    
    fieldsets = (
        (None, {'fields': ('daily_report', 'flight_city')}),
        ('时间信息', {'fields': ('pickup_date', 'cargo_out_time')}),
        ('货物信息', {'fields': ('box_count',)}),
    )


@admin.register(LinehaulReport)
class LinehaulReportAdmin(admin.ModelAdmin):
    list_display = ('daily_report', 'supplier', 'transport_type', 'vehicle_type_count', 'billing_logic')
    list_filter = ('supplier', 'transport_type', 'billing_logic', 'daily_report__report_date')
    search_fields = ('supplier', 'transport_type', 'daily_report__report_date')
    ordering = ('daily_report__report_date', 'supplier')
    
    fieldsets = (
        (None, {'fields': ('daily_report', 'supplier')}),
        ('运输信息', {'fields': ('transport_type', 'vehicle_type_count', 'billing_logic')}),
        ('异常说明', {'fields': ('exception_notes',)}),
    )


@admin.register(ChangeOrderChannel)
class ChangeOrderChannelAdmin(admin.ModelAdmin):
    list_display = ('daily_report', 'channel_name', 'change_order_count')
    list_filter = ('channel_name', 'daily_report__report_date')
    search_fields = ('channel_name', 'daily_report__report_date')
    ordering = ('daily_report__report_date', 'channel_name')
    
    fieldsets = (
        (None, {'fields': ('daily_report', 'channel_name')}),
        ('换单信息', {'fields': ('change_order_count',)}),
        ('异常说明', {'fields': ('exception_notes',)}),
    )


@admin.register(SortingMachineReport)
class SortingMachineReportAdmin(admin.ModelAdmin):
    list_display = ('machine_name', 'machine_type', 'throughput', 'error_rate', 'downtime_hours', 'maintenance_status', 'daily_report')
    list_filter = ('machine_type', 'maintenance_status', 'daily_report__report_date')
    search_fields = ('machine_name', 'machine_type', 'exception_notes')
    ordering = ('daily_report__report_date', 'machine_name')
    
    fieldsets = (
        (None, {'fields': ('daily_report', 'machine_name', 'machine_type')}),
        ('运行数据', {'fields': ('throughput', 'error_rate', 'downtime_hours')}),
        ('维护状态', {'fields': ('maintenance_status',)}),
        ('异常说明', {'fields': ('exception_notes',)}),
    )


@admin.register(EquipmentReport)
class EquipmentReportAdmin(admin.ModelAdmin):
    list_display = ('equipment_name', 'equipment_type', 'status', 'utilization_rate', 'maintenance_hours', 'daily_report')
    list_filter = ('equipment_type', 'status', 'daily_report__report_date')
    search_fields = ('equipment_name', 'equipment_type', 'exception_notes')
    ordering = ('daily_report__report_date', 'equipment_name')
    
    fieldsets = (
        (None, {'fields': ('daily_report', 'equipment_name', 'equipment_type')}),
        ('运行状态', {'fields': ('status', 'utilization_rate', 'maintenance_hours')}),
        ('异常说明', {'fields': ('exception_notes',)}),
    )


@admin.register(QualityReport)
class QualityReportAdmin(admin.ModelAdmin):
    list_display = ('quality_type', 'total_count', 'error_count', 'error_rate', 'daily_report')
    list_filter = ('quality_type', 'daily_report__report_date')
    search_fields = ('quality_type', 'improvement_measures', 'exception_notes')
    ordering = ('daily_report__report_date', 'quality_type')
    
    fieldsets = (
        (None, {'fields': ('daily_report', 'quality_type')}),
        ('质量数据', {'fields': ('total_count', 'error_count', 'error_rate')}),
        ('改进措施', {'fields': ('improvement_measures',)}),
        ('异常说明', {'fields': ('exception_notes',)}),
    )


@admin.register(CostReport)
class CostReportAdmin(admin.ModelAdmin):
    list_display = ('cost_category', 'planned_cost', 'actual_cost', 'variance', 'variance_rate', 'daily_report')
    list_filter = ('cost_category', 'daily_report__report_date')
    search_fields = ('cost_category', 'exception_notes')
    ordering = ('daily_report__report_date', 'cost_category')
    
    fieldsets = (
        (None, {'fields': ('daily_report', 'cost_category')}),
        ('成本数据', {'fields': ('planned_cost', 'actual_cost', 'variance', 'variance_rate')}),
        ('异常说明', {'fields': ('exception_notes',)}),
    )
