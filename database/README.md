# LAX日报系统数据库目录

本目录包含LAX日报系统的数据库相关文件，用于系统安装和初始化。

## 目录结构

```
database/
├── docs/                          # 文档目录
│   ├── database_schema.md         # 数据库结构文档
│   └── installation_guide.md     # 安装说明文档
├── scripts/                       # 脚本目录
│   └── init_database.sh          # 数据库初始化脚本
└── sample_data/                   # 示例数据目录
    └── load_sample_data.py        # 示例数据加载脚本
```

## 文件说明

### 文档文件

- **database_schema.md**: 详细的数据库结构文档，包含所有表结构、字段说明、关系图和索引建议
- **installation_guide.md**: 完整的安装指南，包含环境要求、安装步骤、配置说明和故障排除

### 脚本文件

- **init_database.sh**: 自动化数据库初始化脚本，一键完成数据库设置
- **load_sample_data.py**: 示例数据加载脚本，基于Google Sheet实际数据结构创建示例数据

## 使用方法

### 快速安装

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 运行初始化脚本
./database/scripts/init_database.sh
```

### 手动安装

```bash
# 1. 创建迁移
python manage.py makemigrations

# 2. 应用迁移
python manage.py migrate

# 3. 创建超级用户
python manage.py createsuperuser

# 4. 加载示例数据
python database/sample_data/load_sample_data.py

# 5. 收集静态文件
python manage.py collectstatic
```

## 数据库结构概述

系统基于LAX日报的实际数据结构设计，包含以下主要表：

- **DailyReport**: 日报主表
- **DeliveryReport**: 配送报告表 (基于SAN城市实际数据)
- **WarehouseReport**: 仓内报告表
- **PickupReport**: 揽收报告表
- **AirTransportReport**: 空运报告表
- **LinehaulReport**: 干线报告表
- **ChangeOrderChannel**: 换单渠道表
- **SortingMachineReport**: 分拣机报告表
- **EquipmentReport**: 设备报告表
- **QualityReport**: 质量报告表
- **CostReport**: 成本报告表

## 示例数据

示例数据基于Google Sheet中的实际LAX日报数据创建，包含：

- 最近7天的日报数据
- 4个主要城市 (SAN, LAX, SFO, SEA) 的配送数据
- 各业务模块的完整示例数据
- 真实的数据结构和字段值

## 注意事项

1. 确保Python虚拟环境已激活
2. 确保Django依赖包已安装
3. 初始化前请备份现有数据
4. 生产环境请修改默认密码
5. 定期备份数据库文件

## 技术支持

如有问题，请参考：
- `docs/database_schema.md` - 数据库结构说明
- `docs/installation_guide.md` - 详细安装指南
- Django官方文档
- 项目README文件
