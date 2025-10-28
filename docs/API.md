# LAX日报Portal API文档

## 📋 概述

本文档描述了LAX日报Portal的API接口，包括数据模型、视图接口和API端点。

## 🔗 API端点

### 基础URL
```
http://localhost:8000/
```

### 认证
所有API端点都需要用户认证。使用Django的Session认证。

## 📊 数据模型API

### DailyReport (日报)

#### 字段说明
```python
{
    "id": "integer",           # 主键
    "report_date": "date",     # 报告日期
    "reporter": "integer",     # 报告人ID
    "is_published": "boolean", # 是否发布
    "notes": "string",         # 备注
    "created_at": "datetime",  # 创建时间
    "updated_at": "datetime"   # 更新时间
}
```

#### 相关模型
- `delivery_reports`: 配送报告列表
- `warehouse_reports`: 仓内报告列表
- `pickup_reports`: 揽收报告列表
- `air_transport_reports`: 空运报告列表
- `linehaul_reports`: 干线报告列表
- `change_order_channels`: 换单渠道列表

### DeliveryReport (配送报告)

#### 字段说明
```python
{
    "id": "integer",
    "daily_report": "integer",      # 关联日报ID
    "city": "string",               # 配送城市
    "cargo_volume": "integer",      # 货量
    "box_count": "integer",        # 分箱数
    "open_time": "time",           # 开放时间
    "sorting_error_rate": "decimal", # 分箱错误率
    "sorting_error_count": "integer", # 分箱错误件数
    "delivery_rate_1": "decimal",   # 第1天达成率
    "delivery_rate_2": "decimal",   # 第2天达成率
    "delivery_rate_3": "decimal",   # 第3天达成率
    "stranded_boxes": "integer",    # 现场滞留分箱数
    "exception_notes": "string",    # 异常说明
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### WarehouseReport (仓内报告)

#### 字段说明
```python
{
    "id": "integer",
    "daily_report": "integer",      # 关联日报ID
    "contractor_company": "string",  # 劳务公司
    "attendance_count": "integer",   # 到岗人数
    "work_type": "string",          # 工种
    "actual_hours": "integer",      # 实际工时
    "yesterday_cost": "decimal",    # 昨日成本
    "cost_per_ticket": "decimal",   # 单票成本
    "exception_notes": "string",    # 异常说明
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### PickupReport (揽收报告)

#### 字段说明
```python
{
    "id": "integer",
    "daily_report": "integer",      # 关联日报ID
    "pickup_area": "string",        # 揽收区域
    "pickup_situation": "string",   # 揽收情况
    "return_count": "integer",      # 回库件数
    "exception_notes": "string",    # 异常说明
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### AirTransportReport (空运报告)

#### 字段说明
```python
{
    "id": "integer",
    "daily_report": "integer",      # 关联日报ID
    "flight_city": "string",        # 飞航城市
    "pickup_date": "date",          # 揽收日
    "cargo_out_time": "time",       # 货物出仓时间
    "box_count": "integer",         # 箱数
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### LinehaulReport (干线报告)

#### 字段说明
```python
{
    "id": "integer",
    "daily_report": "integer",      # 关联日报ID
    "supplier": "string",           # 供应商
    "transport_type": "string",     # 发运类型
    "vehicle_type_count": "integer", # 车型及次数
    "billing_logic": "string",      # 计费逻辑
    "exception_notes": "string",    # 异常说明
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### ChangeOrderChannel (换单渠道)

#### 字段说明
```python
{
    "id": "integer",
    "daily_report": "integer",      # 关联日报ID
    "channel_name": "string",       # 换单渠道
    "change_order_count": "integer", # 换单量
    "exception_notes": "string",    # 异常说明
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

## 🌐 视图接口

### 1. 仪表板API

#### 端点
```
GET /portal/api/dashboard/
```

#### 描述
返回最近30天的图表数据，用于仪表板可视化。

#### 响应格式
```json
{
    "labels": ["10-01", "10-02", "10-03", ...],
    "cargo_volume": [1000, 1200, 1100, ...],
    "box_count": [50, 60, 55, ...],
    "error_rate": [0.5, 0.8, 0.6, ...],
    "delivery_rate": [95.0, 98.0, 96.0, ...]
}
```

#### 示例请求
```bash
curl -X GET "http://localhost:8000/portal/api/dashboard/" \
     -H "Cookie: sessionid=your_session_id"
```

### 2. 日报列表

#### 端点
```
GET /portal/daily-reports/
```

#### 描述
返回已发布的日报列表，支持分页。

#### 查询参数
- `page`: 页码（可选，默认1）

#### 响应格式
```json
{
    "page_obj": {
        "number": 1,
        "num_pages": 5,
        "has_previous": false,
        "has_next": true,
        "object_list": [
            {
                "id": 1,
                "report_date": "2025-10-28",
                "reporter": "admin",
                "is_published": true,
                "created_at": "2025-10-28T10:00:00Z"
            }
        ]
    }
}
```

### 3. 日报详情

#### 端点
```
GET /portal/daily-reports/{id}/
```

#### 描述
返回指定日报的详细信息，包括所有相关报告。

#### 路径参数
- `id`: 日报ID

#### 响应格式
```json
{
    "report": {
        "id": 1,
        "report_date": "2025-10-28",
        "reporter": "admin",
        "is_published": true,
        "notes": "测试日报"
    },
    "delivery_reports": [...],
    "warehouse_reports": [...],
    "pickup_reports": [...],
    "air_transport_reports": [...],
    "linehaul_reports": [...],
    "change_order_channels": [...]
}
```

### 4. 业务模块接口

#### 配送管理模块
```
GET /portal/delivery/
```

#### 仓内管理模块
```
GET /portal/warehouse/
```

#### 揽收管理模块
```
GET /portal/pickup/
```

#### 空运管理模块
```
GET /portal/airtransport/
```

#### 干线管理模块
```
GET /portal/linehaul/
```

#### 换单管理模块
```
GET /portal/change-order/
```

#### 描述
返回最近7天的业务数据，用于各模块展示。

#### 响应格式
```json
{
    "delivery_data": [
        {
            "report_date": "2025-10-28",
            "city": "LAX",
            "cargo_volume": 1000,
            "box_count": 50,
            "sorting_error_rate": 0.5,
            "delivery_rate_1": 95.0,
            "delivery_rate_2": 98.0,
            "delivery_rate_3": 99.0,
            "stranded_boxes": 0,
            "exception_notes": ""
        }
    ],
    "date_range": "2025-10-21 至 2025-10-28"
}
```

## 🔐 认证和权限

### 认证方式
- 使用Django Session认证
- 需要先登录获取session cookie

### 权限要求
- 所有API端点都需要用户认证
- 部分功能需要特定权限

### 登录接口
```
POST /login/
```

#### 请求格式
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

#### 响应
- 成功：重定向到仪表板
- 失败：返回登录页面

## 📝 使用示例

### Python示例

```python
import requests

# 登录
session = requests.Session()
login_data = {
    'username': 'your_username',
    'password': 'your_password'
}
response = session.post('http://localhost:8000/login/', data=login_data)

# 获取仪表板数据
dashboard_data = session.get('http://localhost:8000/portal/api/dashboard/')
print(dashboard_data.json())

# 获取日报列表
reports = session.get('http://localhost:8000/portal/daily-reports/')
print(reports.json())
```

### JavaScript示例

```javascript
// 获取仪表板数据
fetch('/portal/api/dashboard/', {
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Dashboard data:', data);
});

// 获取日报列表
fetch('/portal/daily-reports/', {
    credentials: 'include'
})
.then(response => response.json())
.then(data => {
    console.log('Reports:', data);
});
```

## ⚠️ 错误处理

### HTTP状态码
- `200`: 成功
- `302`: 重定向（登录后）
- `403`: 权限不足
- `404`: 资源不存在
- `500`: 服务器错误

### 错误响应格式
```json
{
    "error": "错误描述",
    "code": "ERROR_CODE",
    "details": "详细错误信息"
}
```

## 🔄 版本信息

### API版本
- 当前版本: v1.0.0
- 发布日期: 2025-10-28

### 变更日志
- v1.0.0: 初始API版本

## 📞 支持

如有API相关问题，请联系开发团队或提交GitHub Issue。

---

**注意**: 本文档会随着API的更新而持续维护。建议定期查看最新版本。
