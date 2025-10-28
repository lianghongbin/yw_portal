# LAX日报系统安装说明

## 系统要求

- Python 3.8+
- Django 4.2+
- SQLite3 (默认) 或 PostgreSQL/MySQL
- Git

## 快速安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd Yw_portal
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements/development.txt
```

### 4. 初始化数据库

```bash
# 使用自动化脚本
./database/scripts/init_database.sh

# 或手动执行
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python database/sample_data/load_sample_data.py
python manage.py collectstatic
```

### 5. 启动服务器

```bash
python manage.py runserver
```

访问 http://localhost:8000

## 详细安装步骤

### 环境准备

1. **安装Python 3.8+**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   
   # CentOS/RHEL
   sudo yum install python3 python3-pip
   
   # macOS (使用Homebrew)
   brew install python3
   ```

2. **安装Git**
   ```bash
   # Ubuntu/Debian
   sudo apt install git
   
   # CentOS/RHEL
   sudo yum install git
   
   # macOS
   brew install git
   ```

### 项目设置

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd Yw_portal
   ```

2. **创建虚拟环境**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **升级pip**
   ```bash
   pip install --upgrade pip
   ```

4. **安装依赖包**
   ```bash
   pip install -r requirements/development.txt
   ```

### 数据库配置

#### 使用SQLite (默认)

无需额外配置，Django会自动创建SQLite数据库文件。

#### 使用PostgreSQL

1. **安装PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt install postgresql postgresql-contrib
   
   # CentOS/RHEL
   sudo yum install postgresql-server postgresql-contrib
   ```

2. **创建数据库**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE lax_daily_report;
   CREATE USER lax_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE lax_daily_report TO lax_user;
   \q
   ```

3. **修改设置**
   编辑 `config/settings/base.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'lax_daily_report',
           'USER': 'lax_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

#### 使用MySQL

1. **安装MySQL**
   ```bash
   # Ubuntu/Debian
   sudo apt install mysql-server mysql-client
   
   # CentOS/RHEL
   sudo yum install mysql-server mysql
   ```

2. **创建数据库**
   ```bash
   mysql -u root -p
   CREATE DATABASE lax_daily_report CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'lax_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON lax_daily_report.* TO 'lax_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. **修改设置**
   编辑 `config/settings/base.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'lax_daily_report',
           'USER': 'lax_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

### 数据库初始化

#### 方法1: 使用自动化脚本 (推荐)

```bash
./database/scripts/init_database.sh
```

脚本会自动执行以下操作：
- 检查Python和Django环境
- 创建数据库迁移文件
- 应用数据库迁移
- 创建超级用户 (admin/admin123)
- 加载示例数据
- 收集静态文件
- 验证安装

#### 方法2: 手动执行

1. **创建迁移文件**
   ```bash
   python manage.py makemigrations
   ```

2. **应用迁移**
   ```bash
   python manage.py migrate
   ```

3. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

4. **加载示例数据**
   ```bash
   python database/sample_data/load_sample_data.py
   ```

5. **收集静态文件**
   ```bash
   python manage.py collectstatic
   ```

### 启动服务

```bash
python manage.py runserver
```

默认访问地址: http://localhost:8000

## 访问系统

### 管理后台
- 地址: http://localhost:8000/admin/
- 默认账号: admin
- 默认密码: admin123

### 用户门户
- 地址: http://localhost:8000/portal/
- 需要先注册用户账号

## 生产环境部署

### 使用Gunicorn

1. **安装Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **启动服务**
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```

### 使用Docker

1. **创建Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements/ /app/requirements/
   RUN pip install -r requirements/production.txt
   
   COPY . /app/
   RUN python manage.py collectstatic --noinput
   
   EXPOSE 8000
   CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

2. **构建和运行**
   ```bash
   docker build -t lax-daily-report .
   docker run -p 8000:8000 lax-daily-report
   ```

## 故障排除

### 常见问题

1. **虚拟环境未激活**
   ```bash
   source venv/bin/activate
   ```

2. **依赖包安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements/development.txt
   ```

3. **数据库迁移失败**
   ```bash
   python manage.py migrate --fake-initial
   ```

4. **静态文件收集失败**
   ```bash
   python manage.py collectstatic --noinput --clear
   ```

5. **端口被占用**
   ```bash
   python manage.py runserver 8001
   ```

### 日志查看

```bash
# 查看Django日志
tail -f logs/django.log

# 查看系统日志
journalctl -u your-service-name -f
```

## 更新系统

1. **拉取最新代码**
   ```bash
   git pull origin main
   ```

2. **更新依赖**
   ```bash
   pip install -r requirements/development.txt
   ```

3. **应用数据库迁移**
   ```bash
   python manage.py migrate
   ```

4. **收集静态文件**
   ```bash
   python manage.py collectstatic
   ```

5. **重启服务**
   ```bash
   # 如果使用systemd
   sudo systemctl restart your-service-name
   
   # 如果使用Docker
   docker-compose restart
   ```

## 备份和恢复

### 备份数据库

```bash
# SQLite
cp db.sqlite3 backup/db_$(date +%Y%m%d).sqlite3

# PostgreSQL
pg_dump -h localhost -U lax_user lax_daily_report > backup/db_$(date +%Y%m%d).sql

# MySQL
mysqldump -u lax_user -p lax_daily_report > backup/db_$(date +%Y%m%d).sql
```

### 恢复数据库

```bash
# SQLite
cp backup/db_20250121.sqlite3 db.sqlite3

# PostgreSQL
psql -h localhost -U lax_user lax_daily_report < backup/db_20250121.sql

# MySQL
mysql -u lax_user -p lax_daily_report < backup/db_20250121.sql
```

## 技术支持

如有问题，请查看：
1. 本文档的故障排除部分
2. Django官方文档
3. 项目README文件
4. 联系技术支持团队
