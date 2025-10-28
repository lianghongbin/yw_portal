# LAX日报系统数据库结构文档

## 概述

本文档描述了LAX日报系统的数据库结构，基于Google Sheet中的实际日报数据设计。

## 核心表结构

### 1. DailyReport (日报主表)

存储每日的LAX日报基本信息。

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| id | AutoField | 主键 | 1 |
| report_date | DateField | 报告日期 | 2025-01-21 |
| is_published | BooleanField | 是否发布 | True |
| created_at | DateTimeField | 创建时间 | 2025-01-21 10:00:00 |
| updated_at | DateTimeField | 更新时间 | 2025-01-21 10:00:00 |

### 2. DeliveryReport (配送报告表)

存储各城市的配送数据，基于SAN城市实际数据结构。

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| id | AutoField | 主键 | 1 |
| daily_report_id | ForeignKey | 关联日报ID | 1 |
| city | CharField(10) | 城市代码 | SAN |
| cargo_volume | PositiveIntegerField | 货量 | 1741 |
| box_count | PositiveIntegerField | 分箱数 | 30 |
| open_time | TimeField | 开放时间 | 05:30 |
| site_situation | TextField | 现场情况 | "408 422删除分箱积压" |
| delivery_rate_day1 | DecimalField | 第1天达成率(%) | 78.63 |
| delivery_rate_day2 | DecimalField | 第2天达成率(%) | 87.12 |
| delivery_rate_day3 | DecimalField | 第3天达成率(%) | 96.40 |
| removed_packages | PositiveIntegerField | 包裹移除数 | 20 |
| removal_rate | DecimalField | 移除率(%) | 1.15 |
| exception_notes | TextField | 异常说明 | "异常移除线路：407-4件" |

### 3. WarehouseReport (仓内报告表)

存储仓内管理相关数据。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | AutoField | 主键 |
| daily_report_id | ForeignKey | 关联日报ID |
| warehouse_name | CharField(50) | 仓库名称 |
| inbound_volume | PositiveIntegerField | 入库货量 |
| outbound_volume | PositiveIntegerField | 出库货量 |
| inventory_count | PositiveIntegerField | 库存件数 |
| processing_time | DecimalField | 处理时间(小时) |
| efficiency_rate | DecimalField | 效率(%) |

### 4. PickupReport (揽收报告表)

存储揽收管理相关数据。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | AutoField | 主键 |
| daily_report_id | ForeignKey | 关联日报ID |
| pickup_area | CharField(50) | 揽收区域 |
| scheduled_pickups | PositiveIntegerField | 计划揽收数 |
| completed_pickups | PositiveIntegerField | 完成揽收数 |
| pickup_rate | DecimalField | 揽收达成率(%) |
| avg_pickup_time | DecimalField | 平均揽收时间(分钟) |

### 5. AirTransportReport (空运报告表)

存储空运管理相关数据。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | AutoField | 主键 |
| daily_report_id | ForeignKey | 关联日报ID |
| flight_number | CharField(20) | 航班号 |
| departure_city | CharField(20) | 出发城市 |
| arrival_city | CharField(20) | 到达城市 |
| cargo_weight | DecimalField | 货重(kg) |
| flight_status | CharField(20) | 航班状态 |
| delay_minutes | PositiveIntegerField | 延误分钟数 |

### 6. LinehaulReport (干线报告表)

存储干线运输相关数据。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | AutoField | 主键 |
| daily_report_id | ForeignKey | 关联日报ID |
| route_name | CharField(50) | 路线名称 |
| vehicle_count | PositiveIntegerField | 车辆数量 |
| total_distance | DecimalField | 总距离(km) |
| fuel_consumption | DecimalField | 油耗(L) |
| avg_speed | DecimalField | 平均速度(km/h) |

### 7. ChangeOrderChannel (换单渠道表)

存储换单管理相关数据。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | AutoField | 主键 |
| daily_report_id | ForeignKey | 关联日报ID |
| channel_name | CharField(50) | 渠道名称 |
| change_orders | PositiveIntegerField | 换单数量 |
| success_rate | DecimalField | 成功率(%) |
| avg_process_time | DecimalField | 平均处理时间(分钟) |

### 8. SortingMachineReport (分拣机报告表)

存储分拣机运行数据。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | AutoField | 主键 |
| daily_report_id | ForeignKey | 关联日报ID |
| machine_id | CharField(20) | 机器编号 |
| operating_hours | DecimalField | 运行时间(小时) |
| packages_processed | PositiveIntegerField | 处理包裹数 |
| error_count | PositiveIntegerField | 错误次数 |
| efficiency_rate | DecimalField | 效率(%) |

### 9. EquipmentReport (设备报告表)

存储设备维护相关数据。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | AutoField | 主键 |
| daily_report_id | ForeignKey | 关联日报ID |
| equipment_type | CharField(50) | 设备类型 |
| maintenance_hours | DecimalField | 维护时间(小时) |
| downtime_hours | DecimalField | 停机时间(小时) |
| maintenance_cost | DecimalField | 维护成本 |

### 10. QualityReport (质量报告表)

存储质量监控相关数据。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | AutoField | 主键 |
| daily_report_id | ForeignKey | 关联日报ID |
| quality_check_type | CharField(50) | 质量检查类型 |
| total_checks | PositiveIntegerField | 总检查数 |
| passed_checks | PositiveIntegerField | 通过检查数 |
| quality_rate | DecimalField | 质量率(%) |

### 11. CostReport (成本报告表)

存储成本分析相关数据。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | AutoField | 主键 |
| daily_report_id | ForeignKey | 关联日报ID |
| cost_category | CharField(50) | 成本类别 |
| amount | DecimalField | 金额 |
| currency | CharField(10) | 货币单位 |

## 城市数据说明

系统支持的主要城市：

- **SAN**: 圣地亚哥 (San Diego)
- **LAX**: 洛杉矶 (Los Angeles) 
- **SFO**: 旧金山 (San Francisco)
- **SEA**: 西雅图 (Seattle)

## 数据关系

```
DailyReport (1) -----> (N) DeliveryReport
DailyReport (1) -----> (N) WarehouseReport  
DailyReport (1) -----> (N) PickupReport
DailyReport (1) -----> (N) AirTransportReport
DailyReport (1) -----> (N) LinehaulReport
DailyReport (1) -----> (N) ChangeOrderChannel
DailyReport (1) -----> (N) SortingMachineReport
DailyReport (1) -----> (N) EquipmentReport
DailyReport (1) -----> (N) QualityReport
DailyReport (1) -----> (N) CostReport
```

## 索引建议

为了提高查询性能，建议在以下字段上创建索引：

1. `DailyReport.report_date` - 按日期查询
2. `DeliveryReport.city` - 按城市查询
3. `DeliveryReport.daily_report_id` - 关联查询
4. 所有外键字段

## 数据约束

1. **日期约束**: report_date 不能是未来日期
2. **数值约束**: 所有百分比字段范围 0-100
3. **时间约束**: open_time 格式 HH:MM
4. **城市约束**: city 字段只允许预定义的城市代码

## 扩展性考虑

1. 支持多语言城市名称
2. 支持自定义报告模板
3. 支持历史数据归档
4. 支持数据导入导出功能
