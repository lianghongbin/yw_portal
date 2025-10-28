#!/usr/bin/env python3
"""
LAX日报系统示例数据加载脚本
基于Google Sheet中的实际数据结构创建示例数据
"""

import os
import sys
import django
from datetime import date, timedelta, time
import random

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.portal.models import (
    DailyReport, DeliveryReport, WarehouseReport, PickupReport,
    AirTransportReport, LinehaulReport, ChangeOrderChannel,
    SortingMachineReport, EquipmentReport, QualityReport, CostReport
)
from django.contrib.auth import get_user_model

User = get_user_model()

def create_sample_daily_reports():
    """创建示例日报数据"""
    print("创建示例日报数据...")
    
    # 获取或创建默认报告人
    reporter, created = User.objects.get_or_create(
        username='system_reporter',
        defaults={
            'email': 'system@example.com',
            'first_name': 'System',
            'last_name': 'Reporter',
            'phone': '000-000-0000',
            'department': 'IT',
            'position': 'System',
            'employee_id': 'SYS001',
            'is_employee': True,
            'is_verified': True,
            'last_login_location': 'System',
        }
    )
    if created:
        reporter.set_password('system123')
        reporter.save()
        print(f"  创建默认报告人: {reporter.username}")
    else:
        print(f"  使用现有报告人: {reporter.username}")
    
    # 创建最近7天的日报
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    
    daily_reports = []
    for i in range(7):
        report_date = start_date + timedelta(days=i)
        
        # 检查是否已存在
        if not DailyReport.objects.filter(report_date=report_date).exists():
            daily_report = DailyReport.objects.create(
                report_date=report_date,
                reporter=reporter,
                is_published=True
            )
            daily_reports.append(daily_report)
            print(f"  创建日报: {report_date}")
        else:
            daily_report = DailyReport.objects.get(report_date=report_date)
            daily_reports.append(daily_report)
            print(f"  日报已存在: {report_date}")
    
    return daily_reports

def create_sample_delivery_reports(daily_reports):
    """创建示例配送报告数据"""
    print("创建示例配送报告数据...")
    
    # 基于SAN城市实际数据结构的示例数据
    city_data = {
        'SAN': {
            'base_cargo': 1741,
            'base_boxes': 30,
            'open_time': time(5, 30),
            'delivery_range': (78, 96),
            'removal_range': (15, 25),
            'removal_rate_range': (1.0, 1.5),
            'site_situations': ['408 422删除分箱积压', '货少删除分箱', '分箱积压严重'],
            'typical_issues': ['异常移除线路：407-4件 404-4件', '408和422货少删除分箱', '402和418取货非常慢，催促车队两次']
        },
        'LAX': {
            'base_cargo': 4500,
            'base_boxes': 750,
            'open_time': time(6, 0),
            'delivery_range': (92, 97),
            'removal_range': (50, 80),
            'removal_rate_range': (1.0, 1.8),
            'site_situations': ['分箱积压', '设备故障', '人员不足'],
            'typical_issues': ['航班延误', '海关清关延迟', '交通拥堵']
        },
        'SFO': {
            'base_cargo': 3200,
            'base_boxes': 580,
            'open_time': time(7, 0),
            'delivery_range': (94, 98),
            'removal_range': (35, 60),
            'removal_rate_range': (1.0, 1.9),
            'site_situations': ['雾天影响', '设备故障', '人员不足'],
            'typical_issues': ['雾天影响', '设备故障', '人员不足']
        },
        'SEA': {
            'base_cargo': 2800,
            'base_boxes': 520,
            'open_time': time(7, 30),
            'delivery_range': (93, 97),
            'removal_range': (30, 55),
            'removal_rate_range': (1.0, 2.0),
            'site_situations': ['雨天影响', '道路施工', '分拣延迟'],
            'typical_issues': ['雨天影响', '道路施工', '分拣延迟']
        }
    }
    
    for daily_report in daily_reports:
        for city_code, city_info in city_data.items():
            # 检查是否已存在
            if DeliveryReport.objects.filter(daily_report=daily_report, city=city_code).exists():
                continue
            
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
            
            DeliveryReport.objects.create(
                daily_report=daily_report,
                city=city_code,
                cargo_volume=cargo_volume,
                box_count=box_count,
                open_time=city_info['open_time'],
                site_situation=site_situation,
                delivery_rate_day1=delivery_rate_day1,
                delivery_rate_day2=delivery_rate_day2,
                delivery_rate_day3=delivery_rate_day3,
                removed_packages=removed_packages,
                removal_rate=removal_rate,
                exception_notes=exception_notes
            )
            print(f"  创建配送报告: {city_code} - {daily_report.report_date}")

def create_sample_warehouse_reports(daily_reports):
    """创建示例仓内报告数据"""
    print("创建示例仓内报告数据...")
    
    # 基于LAX日报实际仓内数据
    contractor_data = {
        'HR Solution': {
            'base_attendance': 5,
            'work_type': 'Regular Sorter',
            'base_hours': 40,
            'hourly_rate': 20,
            'base_packages': 4500,
            'sorting_count': 58341,
            'exchange_count': 14211,
            'cost_per_ticket': 0.0110,  # 工时总数 × 20 ÷ (分拣数量 + 换单数量)
            'typical_issues': ['人员不足', '工时超时', '成本控制']
        },
        'Ocean': {
            'base_attendance': 54,
            'work_type': 'Regular Sorter', 
            'base_hours': 545,
            'hourly_rate': 20,
            'base_packages': 38000,
            'sorting_count': 108000,
            'exchange_count': 32000,
            'cost_per_ticket': 0.0779,  # 工时总数 × 20 ÷ (分拣数量 + 换单数量)
            'typical_issues': ['设备故障', '人员调配', '效率提升']
        }
    }
    
    for daily_report in daily_reports:
        for company, company_info in contractor_data.items():
            if WarehouseReport.objects.filter(daily_report=daily_report, contractor_company=company).exists():
                continue
            
            # 基于公司特点生成数据
            attendance_variation = random.uniform(0.9, 1.1)
            hours_variation = random.uniform(0.95, 1.05)
            packages_variation = random.uniform(0.9, 1.1)
            
            attendance_count = int(company_info['base_attendance'] * attendance_variation)
            actual_attendance_count = attendance_count + random.randint(0, 2)
            actual_hours = int(company_info['base_hours'] * hours_variation)
            packages_produced = int(company_info['base_packages'] * packages_variation)
            
            # 异常情况
            has_exception = random.random() < 0.2  # 20%概率有异常
            exception_notes = '无异常'
            if has_exception:
                exception_notes = random.choice(company_info['typical_issues'])
            
            WarehouseReport.objects.create(
                daily_report=daily_report,
                contractor_company=company,
                attendance_count=attendance_count,
                actual_attendance_count=actual_attendance_count,
                work_type=company_info['work_type'],
                actual_hours=actual_hours,
                packages_produced=packages_produced,
                hourly_rate=company_info['hourly_rate'],
                sorting_count=company_info['sorting_count'],
                exchange_count=company_info['exchange_count'],
                cost_per_ticket=company_info['cost_per_ticket'],
                exception_notes=exception_notes,
            )
            print(f"  创建仓内报告: {company} - {daily_report.report_date}")

def create_sample_pickup_reports(daily_reports):
    """创建示例揽收报告数据"""
    print("创建示例揽收报告数据...")
    
    pickup_areas = ['洛杉矶市区', '旧金山湾区', '西雅图市区', '圣地亚哥市区']
    
    for daily_report in daily_reports:
        for area in pickup_areas:
            if PickupReport.objects.filter(daily_report=daily_report, pickup_area=area).exists():
                continue
                
            scheduled = random.randint(50, 200)
            completed = int(scheduled * random.uniform(0.85, 0.98))
            
            PickupReport.objects.create(
                daily_report=daily_report,
                pickup_area=area,
                scheduled_pickups=scheduled,
                completed_pickups=completed,
                pickup_rate=round((completed / scheduled) * 100, 2),
                avg_pickup_time=round(random.uniform(15, 45), 1)
            )
            print(f"  创建揽收报告: {area} - {daily_report.report_date}")

def create_sample_airtransport_reports(daily_reports):
    """创建示例空运报告数据"""
    print("创建示例空运报告数据...")
    
    flights = [
        ('AA123', 'LAX', 'SFO'),
        ('UA456', 'SFO', 'SEA'),
        ('DL789', 'SEA', 'SAN'),
        ('WN321', 'SAN', 'LAX')
    ]
    
    for daily_report in daily_reports:
        for flight_num, dep_city, arr_city in flights:
            if AirTransportReport.objects.filter(daily_report=daily_report, flight_number=flight_num).exists():
                continue
                
            AirTransportReport.objects.create(
                daily_report=daily_report,
                flight_number=flight_num,
                departure_city=dep_city,
                arrival_city=arr_city,
                cargo_weight=round(random.uniform(500, 2000), 2),
                flight_status=random.choice(['正常', '延误', '取消']),
                delay_minutes=random.randint(0, 120) if random.random() < 0.2 else 0
            )
            print(f"  创建空运报告: {flight_num} - {daily_report.report_date}")

def create_sample_linehaul_reports(daily_reports):
    """创建示例干线报告数据"""
    print("创建示例干线报告数据...")
    
    routes = ['LAX-SFO', 'SFO-SEA', 'SEA-SAN', 'SAN-LAX']
    
    for daily_report in daily_reports:
        for route in routes:
            if LinehaulReport.objects.filter(daily_report=daily_report, route_name=route).exists():
                continue
                
            LinehaulReport.objects.create(
                daily_report=daily_report,
                route_name=route,
                vehicle_count=random.randint(3, 8),
                total_distance=round(random.uniform(300, 800), 1),
                fuel_consumption=round(random.uniform(50, 150), 1),
                avg_speed=round(random.uniform(60, 80), 1)
            )
            print(f"  创建干线报告: {route} - {daily_report.report_date}")

def create_sample_change_order_reports(daily_reports):
    """创建示例换单报告数据"""
    print("创建示例换单报告数据...")
    
    channels = ['在线换单', '电话换单', '现场换单', '邮件换单']
    
    for daily_report in daily_reports:
        for channel in channels:
            if ChangeOrderChannel.objects.filter(daily_report=daily_report, channel_name=channel).exists():
                continue
                
            orders = random.randint(5, 50)
            success_rate = round(random.uniform(85, 98), 2)
            
            ChangeOrderChannel.objects.create(
                daily_report=daily_report,
                channel_name=channel,
                change_orders=orders,
                success_rate=success_rate,
                avg_process_time=round(random.uniform(5, 30), 1)
            )
            print(f"  创建换单报告: {channel} - {daily_report.report_date}")

def create_sample_sorting_machine_reports(daily_reports):
    """创建示例分拣机报告数据"""
    print("创建示例分拣机报告数据...")
    
    machines = ['SM001', 'SM002', 'SM003', 'SM004']
    
    for daily_report in daily_reports:
        for machine_id in machines:
            if SortingMachineReport.objects.filter(daily_report=daily_report, machine_id=machine_id).exists():
                continue
                
            SortingMachineReport.objects.create(
                daily_report=daily_report,
                machine_id=machine_id,
                operating_hours=round(random.uniform(8, 16), 1),
                packages_processed=random.randint(500, 2000),
                error_count=random.randint(0, 10),
                efficiency_rate=round(random.uniform(90, 99), 2)
            )
            print(f"  创建分拣机报告: {machine_id} - {daily_report.report_date}")

def create_sample_equipment_reports(daily_reports):
    """创建示例设备报告数据"""
    print("创建示例设备报告数据...")
    
    equipment_types = ['分拣机', '传送带', '叉车', '扫描设备']
    
    for daily_report in daily_reports:
        for eq_type in equipment_types:
            if EquipmentReport.objects.filter(daily_report=daily_report, equipment_type=eq_type).exists():
                continue
                
            EquipmentReport.objects.create(
                daily_report=daily_report,
                equipment_type=eq_type,
                maintenance_hours=round(random.uniform(0.5, 4.0), 1),
                downtime_hours=round(random.uniform(0, 2.0), 1),
                maintenance_cost=round(random.uniform(100, 1000), 2)
            )
            print(f"  创建设备报告: {eq_type} - {daily_report.report_date}")

def create_sample_quality_reports(daily_reports):
    """创建示例质量报告数据"""
    print("创建示例质量报告数据...")
    
    check_types = ['包裹检查', '分拣检查', '配送检查', '设备检查']
    
    for daily_report in daily_reports:
        for check_type in check_types:
            if QualityReport.objects.filter(daily_report=daily_report, quality_check_type=check_type).exists():
                continue
                
            total_checks = random.randint(100, 500)
            passed_checks = int(total_checks * random.uniform(0.92, 0.99))
            
            QualityReport.objects.create(
                daily_report=daily_report,
                quality_check_type=check_type,
                total_checks=total_checks,
                passed_checks=passed_checks,
                quality_rate=round((passed_checks / total_checks) * 100, 2)
            )
            print(f"  创建质量报告: {check_type} - {daily_report.report_date}")

def create_sample_cost_reports(daily_reports):
    """创建示例成本报告数据"""
    print("创建示例成本报告数据...")
    
    cost_categories = ['人工成本', '燃料成本', '设备维护', '运输成本', '管理费用']
    
    for daily_report in daily_reports:
        for category in cost_categories:
            if CostReport.objects.filter(daily_report=daily_report, cost_category=category).exists():
                continue
                
            CostReport.objects.create(
                daily_report=daily_report,
                cost_category=category,
                amount=round(random.uniform(1000, 10000), 2),
                currency='USD'
            )
            print(f"  创建成本报告: {category} - {daily_report.report_date}")

def main():
    """主函数"""
    print("开始加载LAX日报系统示例数据...")
    print("=" * 50)
    
    try:
        # 创建日报
        daily_reports = create_sample_daily_reports()
        print()
        
        # 创建各种报告
        create_sample_delivery_reports(daily_reports)
        print()
        
        create_sample_warehouse_reports(daily_reports)
        print()
        
        create_sample_pickup_reports(daily_reports)
        print()
        
        create_sample_airtransport_reports(daily_reports)
        print()
        
        create_sample_linehaul_reports(daily_reports)
        print()
        
        create_sample_change_order_reports(daily_reports)
        print()
        
        create_sample_sorting_machine_reports(daily_reports)
        print()
        
        create_sample_equipment_reports(daily_reports)
        print()
        
        create_sample_quality_reports(daily_reports)
        print()
        
        create_sample_cost_reports(daily_reports)
        print()
        
        print("=" * 50)
        print("示例数据加载完成！")
        print(f"创建了 {len(daily_reports)} 天的日报数据")
        print("包含所有业务模块的示例数据")
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
