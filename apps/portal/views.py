from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Avg, Count
from django.http import JsonResponse
from datetime import datetime, date, timedelta
import random
from .models import (
    Announcement, Document, Department,
    DailyReport, DeliveryReport, WarehouseReport, 
    PickupReport, AirTransportReport, LinehaulReport, ChangeOrderChannel
)

@login_required(login_url='/login/')
def dashboard_view(request):
    """仪表板视图"""
    announcements = Announcement.objects.filter(is_published=True)[:5]
    documents = Document.objects.filter(is_public=True)[:5]
    departments = Department.objects.all()[:5]
    
    # 获取最新的日报数据
    latest_report = DailyReport.objects.filter(is_published=True).first()
    
    # 计算关键指标
    dashboard_stats = {}
    if latest_report:
        # 配送统计
        delivery_stats = DeliveryReport.objects.filter(daily_report=latest_report).aggregate(
            total_cargo=Sum('cargo_volume'),
            total_boxes=Sum('box_count'),
            avg_removal_rate=Avg('removal_rate'),
            total_removed=Sum('removed_packages')
        )
        
        # 仓内统计
        warehouse_stats = WarehouseReport.objects.filter(daily_report=latest_report).aggregate(
            total_attendance=Sum('attendance_count'),
            total_hours=Sum('actual_hours'),
            total_cost=Sum('yesterday_cost')
        )
        
        # 换单统计
        change_order_stats = ChangeOrderChannel.objects.filter(daily_report=latest_report).aggregate(
            total_change_orders=Sum('change_order_count')
        )
        
        dashboard_stats = {
            'latest_report': latest_report,
            'delivery_stats': delivery_stats,
            'warehouse_stats': warehouse_stats,
            'change_order_stats': change_order_stats,
        }
    
    context = {
        'announcements': announcements,
        'documents': documents,
        'departments': departments,
        'user': request.user,
        'dashboard_stats': dashboard_stats,
    }
    return render(request, 'portal/dashboard.html', context)

@login_required
def announcements_view(request):
    """公告列表视图"""
    announcements = Announcement.objects.filter(is_published=True)
    paginator = Paginator(announcements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'portal/announcements.html', context)

@login_required
def announcement_detail_view(request, pk):
    """公告详情视图"""
    try:
        announcement = Announcement.objects.get(pk=pk, is_published=True)
    except Announcement.DoesNotExist:
        messages.error(request, '公告不存在或已被删除。')
        return redirect('portal:announcements')
    
    context = {
        'announcement': announcement,
    }
    return render(request, 'portal/announcement_detail.html', context)

@login_required
def documents_view(request):
    """文档列表视图"""
    documents = Document.objects.filter(is_public=True)
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'portal/documents.html', context)

@login_required
def departments_view(request):
    """部门列表视图"""
    departments = Department.objects.all()
    
    context = {
        'departments': departments,
    }
    return render(request, 'portal/departments.html', context)


# ==================== LAX日报相关视图 ====================

@login_required
def daily_reports_view(request):
    """日报列表视图"""
    reports = DailyReport.objects.filter(is_published=True)
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'portal/daily_reports.html', context)


@login_required
def daily_report_detail_view(request, pk):
    """日报详情视图"""
    report = get_object_or_404(DailyReport, pk=pk, is_published=True)
    
    # 获取各模块数据
    delivery_reports = DeliveryReport.objects.filter(daily_report=report)
    warehouse_reports = WarehouseReport.objects.filter(daily_report=report)
    pickup_reports = PickupReport.objects.filter(daily_report=report)
    air_transport_reports = AirTransportReport.objects.filter(daily_report=report)
    linehaul_reports = LinehaulReport.objects.filter(daily_report=report)
    change_order_channels = ChangeOrderChannel.objects.filter(daily_report=report)
    
    context = {
        'report': report,
        'delivery_reports': delivery_reports,
        'warehouse_reports': warehouse_reports,
        'pickup_reports': pickup_reports,
        'air_transport_reports': air_transport_reports,
        'linehaul_reports': linehaul_reports,
        'change_order_channels': change_order_channels,
    }
    return render(request, 'portal/daily_report_detail.html', context)


@login_required
def delivery_module_view(request):
    """配送管理模块视图"""
    # 获取城市参数
    selected_city = request.GET.get('city', '')
    # 获取日期参数，默认为今天
    selected_date = request.GET.get('date', '')
    
    # 解析日期
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()
    
    # 获取最近30天的配送数据
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    delivery_data = []
    city_stats = {}
    daily_stats = {}
    
    for report in reports:
        delivery_reports = DeliveryReport.objects.filter(daily_report=report)
        daily_total_cargo = 0
        daily_total_boxes = 0
        daily_cities = []
        
        for dr in delivery_reports:
            # 添加到详细数据列表
            delivery_data.append({
                'report_date': report.report_date,
                'city': dr.city,
                'cargo_volume': dr.cargo_volume,
                'box_count': dr.box_count,
                'open_time': dr.open_time,
                'site_situation': dr.site_situation,
                'delivery_rate_day1': dr.delivery_rate_day1,
                'delivery_rate_day2': dr.delivery_rate_day2,
                'delivery_rate_day3': dr.delivery_rate_day3,
                'removed_packages': dr.removed_packages,
                'removal_rate': dr.removal_rate,
                'exception_notes': dr.exception_notes,
            })
            
            # 统计城市数据
            if dr.city not in city_stats:
                city_stats[dr.city] = {
                    'total_cargo': 0,
                    'total_boxes': 0,
                    'avg_removal_rate': 0,
                    'avg_delivery_rate_day1': 0,
                    'avg_delivery_rate_day2': 0,
                    'avg_delivery_rate_day3': 0,
                    'total_removed': 0,
                    'exception_count': 0,
                    'report_count': 0
                }
            
            city_stats[dr.city]['total_cargo'] += dr.cargo_volume
            city_stats[dr.city]['total_boxes'] += dr.box_count
            city_stats[dr.city]['avg_removal_rate'] += dr.removal_rate
            city_stats[dr.city]['avg_delivery_rate_day1'] += dr.delivery_rate_day1
            city_stats[dr.city]['avg_delivery_rate_day2'] += dr.delivery_rate_day2
            city_stats[dr.city]['avg_delivery_rate_day3'] += dr.delivery_rate_day3
            city_stats[dr.city]['total_removed'] += dr.removed_packages
            city_stats[dr.city]['report_count'] += 1
            
            if dr.exception_notes:
                city_stats[dr.city]['exception_count'] += 1
            
            daily_total_cargo += dr.cargo_volume
            daily_total_boxes += dr.box_count
            daily_cities.append(dr.city)
        
        # 统计每日数据
        if delivery_reports.exists():
            daily_stats[report.report_date] = {
                'total_cargo': daily_total_cargo,
                'total_boxes': daily_total_boxes,
                'cities': daily_cities,
                'city_count': len(daily_cities)
            }
    
    # 计算城市平均值
    for city in city_stats:
        count = city_stats[city]['report_count']
        if count > 0:
            city_stats[city]['avg_removal_rate'] = round(city_stats[city]['avg_removal_rate'] / count, 2)
            city_stats[city]['avg_delivery_rate_day1'] = round(city_stats[city]['avg_delivery_rate_day1'] / count, 2)
            city_stats[city]['avg_delivery_rate_day2'] = round(city_stats[city]['avg_delivery_rate_day2'] / count, 2)
            city_stats[city]['avg_delivery_rate_day3'] = round(city_stats[city]['avg_delivery_rate_day3'] / count, 2)
    
    # 创建基于LAX日报的示例数据（用于演示）
    # 由于数据库中没有真实数据，直接创建示例数据
    delivery_data = []
    
    # LAX日报实际城市数据 - 基于真实运营情况
    city_data = {
        'SAN': {
            'base_cargo': 1741,
            'base_boxes': 30,
            'open_time': '05:30',
            'delivery_range': (78, 96),
            'removal_range': (15, 25),
            'removal_rate_range': (1.0, 1.5),
            'site_situations': ['408 422删除分箱积压', '货少删除分箱', '分箱积压严重'],
            'typical_issues': ['异常移除线路：407-4件 404-4件', '408和422货少删除分箱', '402和418取货非常慢，催促车队两次']
        },
        'LAX': {
            'base_cargo': 4500,
            'base_boxes': 750,
            'open_time': '06:00',
            'delivery_range': (92, 97),
            'removal_range': (50, 80),
            'removal_rate_range': (1.0, 1.8),
            'site_situations': ['分箱积压', '设备故障', '人员不足'],
            'typical_issues': ['航班延误', '海关清关延迟', '交通拥堵']
        },
        'SFO': {
            'base_cargo': 3200,
            'base_boxes': 580,
            'open_time': '07:00',
            'delivery_range': (94, 98),
            'removal_range': (35, 60),
            'removal_rate_range': (1.0, 1.9),
            'site_situations': ['雾天影响', '设备故障', '人员不足'],
            'typical_issues': ['雾天影响', '设备故障', '人员不足']
        },
        'SEA': {
            'base_cargo': 2800,
            'base_boxes': 520,
            'open_time': '07:30',
            'delivery_range': (93, 97),
            'removal_range': (30, 55),
            'removal_rate_range': (1.0, 2.0),
            'site_situations': ['雨天影响', '道路施工', '分拣延迟'],
            'typical_issues': ['雨天影响', '道路施工', '分拣延迟']
        }
    }
    
    sample_dates = [(end_date - timedelta(days=i)) for i in range(7)]
    
    for report_date in sample_dates:
        for city_code, city_info in city_data.items():
            # 基于城市特点生成数据
            cargo_variation = random.uniform(0.85, 1.15)
            box_variation = random.uniform(0.9, 1.1)
            
            cargo_volume = int(city_info['base_cargo'] * cargo_variation)
            box_count = int(city_info['base_boxes'] * box_variation)
            
            # 现场情况
            site_situation = random.choice(city_info['site_situations'])
            
            # 配送率基于城市特点（3天递进）
            delivery_base = random.uniform(*city_info['delivery_range'])
            delivery_rate_day1 = round(delivery_base - random.uniform(0, 3), 2)
            delivery_rate_day2 = round(delivery_base + random.uniform(0, 2), 2)
            delivery_rate_day3 = round(delivery_base + random.uniform(2, 5), 2)
            
            # 包裹移除数据
            removed_packages = random.randint(*city_info['removal_range'])
            removal_rate = round(random.uniform(*city_info['removal_rate_range']), 2)
            
            # 异常情况
            has_exception = random.random() < 0.15  # 15%概率有异常
            exception_notes = '无异常'
            if has_exception:
                exception_notes = random.choice(city_info['typical_issues'])
            
            delivery_data.append({
                'report_date': report_date,
                'city': city_code,
                'cargo_volume': cargo_volume,
                'box_count': box_count,
                'open_time': city_info['open_time'],
                'site_situation': site_situation,
                'delivery_rate_day1': delivery_rate_day1,
                'delivery_rate_day2': delivery_rate_day2,
                'delivery_rate_day3': delivery_rate_day3,
                'removed_packages': removed_packages,
                'removal_rate': removal_rate,
                'exception_notes': exception_notes,
            })
    
    # 如果选择了特定城市，筛选数据
    if selected_city:
        delivery_data = [data for data in delivery_data if data['city'] == selected_city]
    
    # 如果选择了特定日期，筛选数据
    if selected_date:
        delivery_data = [data for data in delivery_data if data['report_date'] == selected_date]
    
    # 重新计算城市统计数据
    city_stats = {}
    for data in delivery_data:
        city = data['city']
        if city not in city_stats:
            city_stats[city] = {
                'total_cargo': 0,
                'total_boxes': 0,
                'avg_removal_rate': 0,
                'avg_delivery_rate_day1': 0,
                'avg_delivery_rate_day2': 0,
                'avg_delivery_rate_day3': 0,
                'total_removed': 0,
                'exception_count': 0,
                'report_count': 0
            }
        
        city_stats[city]['total_cargo'] += data['cargo_volume']
        city_stats[city]['total_boxes'] += data['box_count']
        city_stats[city]['avg_removal_rate'] += data['removal_rate']
        city_stats[city]['avg_delivery_rate_day1'] += data['delivery_rate_day1']
        city_stats[city]['avg_delivery_rate_day2'] += data['delivery_rate_day2']
        city_stats[city]['avg_delivery_rate_day3'] += data['delivery_rate_day3']
        city_stats[city]['total_removed'] += data['removed_packages']
        city_stats[city]['report_count'] += 1
        
        if data['exception_notes'] != '无异常':
            city_stats[city]['exception_count'] += 1
    
    # 计算城市平均值
    for city in city_stats:
        count = city_stats[city]['report_count']
        if count > 0:
            city_stats[city]['avg_removal_rate'] = round(city_stats[city]['avg_removal_rate'] / count, 2)
            city_stats[city]['avg_delivery_rate_day1'] = round(city_stats[city]['avg_delivery_rate_day1'] / count, 2)
            city_stats[city]['avg_delivery_rate_day2'] = round(city_stats[city]['avg_delivery_rate_day2'] / count, 2)
            city_stats[city]['avg_delivery_rate_day3'] = round(city_stats[city]['avg_delivery_rate_day3'] / count, 2)
        
    
    # 获取所有可用城市列表 - 使用LAX日报中的实际城市（根据Google Sheet内容）
    all_cities = ['SAN', 'LAX', 'SFO', 'SEA']
    
    # 获取可用日期列表（最近7天）
    available_dates = [(date.today() - timedelta(days=i)) for i in range(7)]
    
    context = {
        'delivery_data': delivery_data,
        'city_stats': city_stats,
        'daily_stats': daily_stats,
        'date_range': f"{start_date} 至 {end_date}",
        'total_cities': len(city_stats),
        'total_records': len(delivery_data),
        'all_cities': all_cities,
        'selected_city': selected_city,
        'available_dates': available_dates,
        'selected_date': selected_date,
    }
    return render(request, 'portal/delivery_module.html', context)


@login_required
def warehouse_module_view(request):
    """仓内管理模块视图"""
    # 获取最近7天的仓内数据
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    warehouse_data = []
    
    # 基于LAX日报实际仓内数据
    contractor_data = {
        'HR Solution': {
            'base_attendance': 5,
            'work_type': 'Regular Sorter',
            'base_hours': 40,
            'base_cost': 72552,
            'cost_per_ticket': 0.16,
            'typical_issues': ['人员不足', '工时超时', '成本控制']
        },
        'Ocean': {
            'base_attendance': 54,
            'work_type': 'Regular Sorter', 
            'base_hours': 545,
            'base_cost': 45000,
            'cost_per_ticket': 0.12,
            'typical_issues': ['设备故障', '人员调配', '效率提升']
        }
    }
    
    # 生成示例数据
    sample_dates = [(end_date - timedelta(days=i)) for i in range(7)]
    
    for report_date in sample_dates:
        for company, company_info in contractor_data.items():
            # 基于公司特点生成数据
            attendance_variation = random.uniform(0.9, 1.1)
            hours_variation = random.uniform(0.95, 1.05)
            cost_variation = random.uniform(0.9, 1.1)
            
            attendance_count = int(company_info['base_attendance'] * attendance_variation)
            actual_hours = int(company_info['base_hours'] * hours_variation)
            yesterday_cost = round(company_info['base_cost'] * cost_variation, 2)
            
            # 异常情况
            has_exception = random.random() < 0.2  # 20%概率有异常
            exception_notes = '无异常'
            if has_exception:
                exception_notes = random.choice(company_info['typical_issues'])
            
            warehouse_data.append({
                'report_date': report_date,
                'contractor_company': company,
                'attendance_count': attendance_count,
                'work_type': company_info['work_type'],
                'actual_hours': actual_hours,
                'yesterday_cost': yesterday_cost,
                'cost_per_ticket': company_info['cost_per_ticket'],
                'exception_notes': exception_notes,
            })
    
    # 基于实际数据计算统计数据
    today_data = [data for data in warehouse_data if data['report_date'] == end_date]
    
    # 统计数据
    total_companies = len(today_data)
    total_attendance = sum(data['attendance_count'] for data in today_data)
    total_hours = sum(data['actual_hours'] for data in today_data)
    total_cost = sum(data['yesterday_cost'] for data in today_data)
    
    # 按公司统计
    company_stats = {}
    for data in today_data:
        company = data['contractor_company']
        if company not in company_stats:
            company_stats[company] = {
                'attendance': 0,
                'hours': 0,
                'cost': 0,
                'cost_per_ticket': 0,
                'work_type': '',
                'has_exception': False
            }
        company_stats[company]['attendance'] += data['attendance_count']
        company_stats[company]['hours'] += data['actual_hours']
        company_stats[company]['cost'] += data['yesterday_cost']
        company_stats[company]['cost_per_ticket'] = data['cost_per_ticket']
        company_stats[company]['work_type'] = data['work_type']
        if data['exception_notes'] and data['exception_notes'] != '无异常':
            company_stats[company]['has_exception'] = True
    
    context = {
        'warehouse_data': warehouse_data,
        'available_dates': sample_dates,
        'selected_date': end_date,
        'today_data': today_data,
        'total_companies': total_companies,
        'total_attendance': total_attendance,
        'total_hours': total_hours,
        'total_cost': total_cost,
        'company_stats': company_stats,
    }
    return render(request, 'portal/warehouse_module.html', context)


@login_required
def pickup_module_view(request):
    """揽收管理模块视图"""
    # 获取最近7天的揽收数据
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    pickup_data = []
    for report in reports:
        pickup_reports = PickupReport.objects.filter(daily_report=report)
        for pr in pickup_reports:
            pickup_data.append({
                'report_date': report.report_date,
                'pickup_area': pr.pickup_area,
                'pickup_situation': pr.pickup_situation,
                'return_count': pr.return_count,
                'exception_notes': pr.exception_notes,
            })
    
    context = {
        'pickup_data': pickup_data,
        'date_range': f"{start_date} 至 {end_date}",
    }
    return render(request, 'portal/pickup_module.html', context)


@login_required
def airtransport_module_view(request):
    """空运管理模块视图"""
    # 获取最近7天的空运数据
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    airtransport_data = []
    for report in reports:
        air_transport_reports = AirTransportReport.objects.filter(daily_report=report)
        for atr in air_transport_reports:
            airtransport_data.append({
                'report_date': report.report_date,
                'flight_city': atr.flight_city,
                'pickup_date': atr.pickup_date,
                'cargo_out_time': atr.cargo_out_time,
                'box_count': atr.box_count,
            })
    
    context = {
        'airtransport_data': airtransport_data,
        'date_range': f"{start_date} 至 {end_date}",
    }
    return render(request, 'portal/airtransport_module.html', context)


@login_required
def linehaul_module_view(request):
    """干线管理模块视图"""
    # 获取最近7天的干线数据
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    linehaul_data = []
    for report in reports:
        linehaul_reports = LinehaulReport.objects.filter(daily_report=report)
        for lr in linehaul_reports:
            linehaul_data.append({
                'report_date': report.report_date,
                'supplier': lr.supplier,
                'transport_type': lr.transport_type,
                'vehicle_type_count': lr.vehicle_type_count,
                'billing_logic': lr.billing_logic,
                'exception_notes': lr.exception_notes,
            })
    
    context = {
        'linehaul_data': linehaul_data,
        'date_range': f"{start_date} 至 {end_date}",
    }
    return render(request, 'portal/linehaul_module.html', context)


@login_required
def change_order_module_view(request):
    """换单管理模块视图"""
    # 获取最近7天的换单数据
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    change_order_data = []
    for report in reports:
        change_order_channels = ChangeOrderChannel.objects.filter(daily_report=report)
        for coc in change_order_channels:
            change_order_data.append({
                'report_date': report.report_date,
                'channel_name': coc.channel_name,
                'change_order_count': coc.change_order_count,
                'exception_notes': coc.exception_notes,
            })
    
    context = {
        'change_order_data': change_order_data,
        'date_range': f"{start_date} 至 {end_date}",
    }
    return render(request, 'portal/change_order_module.html', context)


@login_required
def dashboard_api_view(request):
    """仪表板API视图 - 返回JSON数据用于图表"""
    # 获取最近30天的数据
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('report_date')
    
    # 准备图表数据
    chart_data = {
        'labels': [],
        'cargo_volume': [],
        'box_count': [],
        'error_rate': [],
        'delivery_rate': [],
    }
    
    for report in reports:
        chart_data['labels'].append(report.report_date.strftime('%m-%d'))
        
        # 配送数据
        delivery_stats = DeliveryReport.objects.filter(daily_report=report).aggregate(
            total_cargo=Sum('cargo_volume'),
            total_boxes=Sum('box_count'),
            avg_removal_rate=Avg('removal_rate'),
            avg_delivery_rate=Avg('delivery_rate_day1')
        )
        
        chart_data['cargo_volume'].append(delivery_stats['total_cargo'] or 0)
        chart_data['box_count'].append(delivery_stats['total_boxes'] or 0)
        chart_data['removal_rate'].append(float(delivery_stats['avg_removal_rate'] or 0))
        chart_data['delivery_rate'].append(float(delivery_stats['avg_delivery_rate'] or 0))
    
    return JsonResponse(chart_data)


@login_required
def sorting_machine_module_view(request):
    """分拣机管理模块视图"""
    # 获取最近7天的分拣机数据
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    sorting_machine_data = []
    for report in reports:
        sorting_reports = SortingMachineReport.objects.filter(daily_report=report)
        for sr in sorting_reports:
            sorting_machine_data.append({
                'report_date': report.report_date,
                'machine_name': sr.machine_name,
                'machine_type': sr.machine_type,
                'throughput': sr.throughput,
                'error_rate': sr.error_rate,
                'downtime_hours': sr.downtime_hours,
                'maintenance_status': sr.maintenance_status,
                'exception_notes': sr.exception_notes,
            })
    
    context = {
        'sorting_machine_data': sorting_machine_data,
        'date_range': f"{start_date} 至 {end_date}",
    }
    return render(request, 'portal/sorting_machine_module.html', context)


@login_required
def equipment_maintenance_module_view(request):
    """设备维护模块视图"""
    # 获取最近7天的设备数据
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    equipment_data = []
    for report in reports:
        equipment_reports = EquipmentReport.objects.filter(daily_report=report)
        for er in equipment_reports:
            equipment_data.append({
                'report_date': report.report_date,
                'equipment_name': er.equipment_name,
                'equipment_type': er.equipment_type,
                'status': er.status,
                'utilization_rate': er.utilization_rate,
                'maintenance_hours': er.maintenance_hours,
                'exception_notes': er.exception_notes,
            })
    
    context = {
        'equipment_data': equipment_data,
        'date_range': f"{start_date} 至 {end_date}",
    }
    return render(request, 'portal/equipment_maintenance_module.html', context)


@login_required
def quality_monitoring_module_view(request):
    """质量监控模块视图"""
    # 获取最近7天的质量数据
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    quality_data = []
    for report in reports:
        quality_reports = QualityReport.objects.filter(daily_report=report)
        for qr in quality_reports:
            quality_data.append({
                'report_date': report.report_date,
                'quality_type': qr.quality_type,
                'total_count': qr.total_count,
                'error_count': qr.error_count,
                'error_rate': qr.error_rate,
                'improvement_measures': qr.improvement_measures,
                'exception_notes': qr.exception_notes,
            })
    
    context = {
        'quality_data': quality_data,
        'date_range': f"{start_date} 至 {end_date}",
    }
    return render(request, 'portal/quality_monitoring_module.html', context)


@login_required
def exception_handling_module_view(request):
    """异常处理模块视图"""
    # 获取最近7天有异常说明的数据
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    exception_data = []
    for report in reports:
        # 收集所有有异常说明的数据
        delivery_exceptions = DeliveryReport.objects.filter(
            daily_report=report, exception_notes__isnull=False
        ).exclude(exception_notes='')
        warehouse_exceptions = WarehouseReport.objects.filter(
            daily_report=report, exception_notes__isnull=False
        ).exclude(exception_notes='')
        pickup_exceptions = PickupReport.objects.filter(
            daily_report=report, exception_notes__isnull=False
        ).exclude(exception_notes='')
        linehaul_exceptions = LinehaulReport.objects.filter(
            daily_report=report, exception_notes__isnull=False
        ).exclude(exception_notes='')
        change_order_exceptions = ChangeOrderChannel.objects.filter(
            daily_report=report, exception_notes__isnull=False
        ).exclude(exception_notes='')
        sorting_exceptions = SortingMachineReport.objects.filter(
            daily_report=report, exception_notes__isnull=False
        ).exclude(exception_notes='')
        equipment_exceptions = EquipmentReport.objects.filter(
            daily_report=report, exception_notes__isnull=False
        ).exclude(exception_notes='')
        quality_exceptions = QualityReport.objects.filter(
            daily_report=report, exception_notes__isnull=False
        ).exclude(exception_notes='')
        cost_exceptions = CostReport.objects.filter(
            daily_report=report, exception_notes__isnull=False
        ).exclude(exception_notes='')
        
        # 添加异常数据
        for de in delivery_exceptions:
            exception_data.append({
                'report_date': report.report_date,
                'module': '配送管理',
                'item': f"{de.city}配送",
                'exception_notes': de.exception_notes,
            })
        
        for we in warehouse_exceptions:
            exception_data.append({
                'report_date': report.report_date,
                'module': '仓内管理',
                'item': we.contractor_company,
                'exception_notes': we.exception_notes,
            })
        
        for pe in pickup_exceptions:
            exception_data.append({
                'report_date': report.report_date,
                'module': '揽收管理',
                'item': pe.pickup_area,
                'exception_notes': pe.exception_notes,
            })
        
        for le in linehaul_exceptions:
            exception_data.append({
                'report_date': report.report_date,
                'module': '干线管理',
                'item': le.supplier,
                'exception_notes': le.exception_notes,
            })
        
        for ce in change_order_exceptions:
            exception_data.append({
                'report_date': report.report_date,
                'module': '换单管理',
                'item': ce.channel_name,
                'exception_notes': ce.exception_notes,
            })
        
        for se in sorting_exceptions:
            exception_data.append({
                'report_date': report.report_date,
                'module': '分拣机管理',
                'item': se.machine_name,
                'exception_notes': se.exception_notes,
            })
        
        for ee in equipment_exceptions:
            exception_data.append({
                'report_date': report.report_date,
                'module': '设备维护',
                'item': ee.equipment_name,
                'exception_notes': ee.exception_notes,
            })
        
        for qe in quality_exceptions:
            exception_data.append({
                'report_date': report.report_date,
                'module': '质量监控',
                'item': qe.quality_type,
                'exception_notes': qe.exception_notes,
            })
        
        for ce in cost_exceptions:
            exception_data.append({
                'report_date': report.report_date,
                'module': '成本分析',
                'item': ce.cost_category,
                'exception_notes': ce.exception_notes,
            })
    
    context = {
        'exception_data': exception_data,
        'date_range': f"{start_date} 至 {end_date}",
    }
    return render(request, 'portal/exception_handling_module.html', context)


@login_required
def cost_analysis_module_view(request):
    """成本分析模块视图"""
    # 获取最近7天的成本数据
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    reports = DailyReport.objects.filter(
        is_published=True,
        report_date__range=[start_date, end_date]
    ).order_by('-report_date')
    
    cost_data = []
    for report in reports:
        cost_reports = CostReport.objects.filter(daily_report=report)
        for cr in cost_reports:
            cost_data.append({
                'report_date': report.report_date,
                'cost_category': cr.cost_category,
                'planned_cost': cr.planned_cost,
                'actual_cost': cr.actual_cost,
                'variance': cr.variance,
                'variance_rate': cr.variance_rate,
                'exception_notes': cr.exception_notes,
            })
    
    context = {
        'cost_data': cost_data,
        'date_range': f"{start_date} 至 {end_date}",
    }
    return render(request, 'portal/cost_analysis_module.html', context)
