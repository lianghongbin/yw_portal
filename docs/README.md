# LAX日报Portal用户文档

## 📋 概述

LAX日报Portal是一个基于Django的Web应用程序，用于管理和展示LAX物流配送中心的日常运营报告。该系统将传统的Excel日报转换为现代化的Web应用，提供更好的数据管理和分析能力。

## 🚀 功能特性

### 核心功能
- **日报管理**: 创建、编辑、发布和管理LAX日报
- **数据可视化**: 使用Chart.js展示关键指标趋势
- **多模块展示**: 配送、仓内、揽收、空运、干线、换单等业务模块
- **响应式设计**: 支持桌面端和移动端访问
- **权限管理**: 基于角色的访问控制

### 业务模块
1. **配送管理模块**
   - 各城市配送状态监控
   - 配送时效达成率分析
   - 分拣错误率统计
   - 现场滞留情况跟踪

2. **仓内管理模块**
   - 劳务公司出勤统计
   - 工时成本分析
   - BBC成本计算
   - 换单渠道管理

3. **揽收管理模块**
   - 各区域揽收情况
   - 回库件数统计
   - 异常情况处理

4. **空运管理模块**
   - 飞航城市管理
   - 货物出仓时间跟踪
   - 箱数统计

5. **干线管理模块**
   - 供应商管理
   - 车型及次数统计
   - 计费逻辑管理

6. **换单管理模块**
   - 换单渠道统计
   - 换单量分析
   - 异常情况监控

## 🏗️ 系统架构

### 技术栈
- **后端**: Django 4.2.7
- **前端**: Bootstrap 5, Chart.js
- **数据库**: SQLite (开发环境)
- **认证**: Django内置认证系统
- **权限**: Django权限系统

### 项目结构
```
Yw_portal/
├── apps/
│   ├── authentication/     # 认证应用
│   ├── core/             # 核心应用
│   ├── portal/           # 门户应用
│   └── rbac/            # 权限管理应用
├── config/               # 项目配置
├── frontend/             # 前端模板
├── tests/               # 测试文件
└── requirements/        # 依赖管理
```

## 📊 数据模型

### 核心模型
- **DailyReport**: 日报主表
- **DeliveryReport**: 配送报告
- **WarehouseReport**: 仓内报告
- **PickupReport**: 揽收报告
- **AirTransportReport**: 空运报告
- **LinehaulReport**: 干线报告
- **ChangeOrderChannel**: 换单渠道

### 模型关系
```
DailyReport (1) -----> (N) DeliveryReport
DailyReport (1) -----> (N) WarehouseReport
DailyReport (1) -----> (N) PickupReport
DailyReport (1) -----> (N) AirTransportReport
DailyReport (1) -----> (N) LinehaulReport
DailyReport (1) -----> (N) ChangeOrderChannel
```

## 🔧 安装和配置

### 环境要求
- Python 3.8+
- Django 4.2.7
- SQLite 3

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd Yw_portal
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements/development.txt
```

4. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **创建超级用户**
```bash
python manage.py createsuperuser
```

6. **运行开发服务器**
```bash
python manage.py runserver
```

## 👥 用户指南

### 登录系统
1. 访问 `http://localhost:8000/login/`
2. 输入用户名和密码
3. 点击登录按钮

### 查看仪表板
1. 登录后自动跳转到仪表板
2. 查看LAX日报关键指标
3. 使用快速导航访问各业务模块

### 查看日报
1. 点击"日报列表"菜单
2. 浏览已发布的日报
3. 点击"查看详情"查看完整报告

### 访问业务模块
1. 使用仪表板上的快速导航按钮
2. 或通过左侧菜单访问各模块
3. 查看最近7天的业务数据

### 数据可视化
- 仪表板提供4个图表：
  - 货量趋势图
  - 分箱数趋势图
  - 错误率趋势图
  - 配送达成率图

## 🔐 权限管理

### 用户角色
- **管理员**: 全部功能访问权限
- **运营人员**: 查看和编辑权限
- **普通用户**: 只读权限

### 权限设置
1. 登录Django Admin (`/admin/`)
2. 在"用户"部分管理用户权限
3. 在"组"部分设置角色权限

## 📱 移动端支持

### 响应式设计
- 支持手机、平板、桌面设备
- 自适应布局和字体大小
- 移动端专用菜单

### 移动端功能
- 侧边栏菜单切换
- 触摸友好的按钮和链接
- 优化的表格显示

## 🧪 测试

### 运行测试
```bash
python manage.py test tests.test_portal
```

### 测试覆盖
- 模型测试
- 视图测试
- URL测试
- Admin测试

## 🚀 部署

### 生产环境配置
1. 修改 `config/settings/production.py`
2. 配置数据库（PostgreSQL/MySQL）
3. 设置静态文件服务
4. 配置Web服务器（Nginx/Apache）

### Docker部署
```bash
docker build -t yw-portal .
docker run -p 8000:8000 yw-portal
```

## 🔧 开发指南

### 添加新功能
1. 创建新的模型
2. 编写视图和URL
3. 创建模板
4. 编写测试
5. 更新文档

### 代码规范
- 遵循PEP 8
- 使用有意义的变量名
- 添加适当的注释
- 编写单元测试

## 📞 支持和反馈

### 问题报告
- 通过GitHub Issues报告问题
- 提供详细的错误信息
- 包含复现步骤

### 功能请求
- 通过GitHub Issues提交功能请求
- 描述使用场景和预期效果

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🔄 更新日志

### v1.0.0 (2025-10-28)
- 初始版本发布
- 实现LAX日报核心功能
- 支持6个业务模块
- 集成数据可视化
- 响应式设计支持

---

**注意**: 本文档会随着系统功能的更新而持续维护。如有疑问，请联系开发团队。
