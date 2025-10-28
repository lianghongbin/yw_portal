#!/bin/bash

# LAX日报系统数据库初始化脚本
# 用于在安装时初始化数据库

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Python环境
check_python() {
    log_info "检查Python环境..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装，请先安装Python3"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    log_success "Python版本: $PYTHON_VERSION"
}

# 检查虚拟环境
check_venv() {
    log_info "检查虚拟环境..."
    
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        log_success "虚拟环境已激活: $VIRTUAL_ENV"
    else
        log_warning "虚拟环境未激活，尝试激活..."
        if [ -f "venv/bin/activate" ]; then
            source venv/bin/activate
            log_success "虚拟环境已激活"
        else
            log_error "虚拟环境不存在，请先创建虚拟环境"
            exit 1
        fi
    fi
}

# 检查Django环境
check_django() {
    log_info "检查Django环境..."
    
    if ! python3 -c "import django" 2>/dev/null; then
        log_error "Django未安装，请先安装依赖包"
        exit 1
    fi
    
    DJANGO_VERSION=$(python3 -c "import django; print(django.get_version())")
    log_success "Django版本: $DJANGO_VERSION"
}

# 创建数据库迁移
create_migrations() {
    log_info "创建数据库迁移文件..."
    
    python3 manage.py makemigrations
    
    if [ $? -eq 0 ]; then
        log_success "迁移文件创建成功"
    else
        log_error "迁移文件创建失败"
        exit 1
    fi
}

# 应用数据库迁移
apply_migrations() {
    log_info "应用数据库迁移..."
    
    python3 manage.py migrate
    
    if [ $? -eq 0 ]; then
        log_success "数据库迁移应用成功"
    else
        log_error "数据库迁移应用失败"
        exit 1
    fi
}

# 创建超级用户
create_superuser() {
    log_info "创建超级用户..."
    
    # 检查是否已存在超级用户
    SUPERUSER_EXISTS=$(python3 manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print('True' if User.objects.filter(is_superuser=True).exists() else 'False')
")
    
    if [ "$SUPERUSER_EXISTS" = "True" ]; then
        log_warning "超级用户已存在，跳过创建"
        return
    fi
    
    # 创建超级用户
    python3 manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('超级用户创建成功: admin/admin123')
else:
    print('超级用户admin已存在')
"
    
    log_success "超级用户创建完成"
}

# 加载示例数据
load_sample_data() {
    log_info "加载示例数据..."
    
    if [ -f "database/sample_data/load_sample_data.py" ]; then
        python3 database/sample_data/load_sample_data.py
        log_success "示例数据加载完成"
    else
        log_warning "示例数据脚本不存在，跳过"
    fi
}

# 收集静态文件
collect_static() {
    log_info "收集静态文件..."
    
    python3 manage.py collectstatic --noinput
    
    if [ $? -eq 0 ]; then
        log_success "静态文件收集完成"
    else
        log_warning "静态文件收集失败"
    fi
}

# 验证安装
verify_installation() {
    log_info "验证安装..."
    
    # 检查数据库连接
    python3 manage.py check --database default
    
    if [ $? -eq 0 ]; then
        log_success "数据库连接正常"
    else
        log_error "数据库连接失败"
        exit 1
    fi
    
    # 检查Django配置
    python3 manage.py check
    
    if [ $? -eq 0 ]; then
        log_success "Django配置检查通过"
    else
        log_error "Django配置检查失败"
        exit 1
    fi
}

# 显示安装信息
show_installation_info() {
    log_success "=========================================="
    log_success "LAX日报系统安装完成！"
    log_success "=========================================="
    echo ""
    log_info "访问信息:"
    echo "  - 管理后台: http://localhost:8000/admin/"
    echo "  - 用户门户: http://localhost:8000/portal/"
    echo ""
    log_info "默认账号:"
    echo "  - 用户名: admin"
    echo "  - 密码: admin123"
    echo ""
    log_info "启动服务器:"
    echo "  python3 manage.py runserver"
    echo ""
    log_warning "请及时修改默认密码！"
}

# 主函数
main() {
    log_info "开始初始化LAX日报系统数据库..."
    echo ""
    
    check_python
    check_venv
    check_django
    echo ""
    
    create_migrations
    apply_migrations
    echo ""
    
    create_superuser
    echo ""
    
    load_sample_data
    echo ""
    
    collect_static
    echo ""
    
    verify_installation
    echo ""
    
    show_installation_info
}

# 错误处理
trap 'log_error "脚本执行失败，请检查错误信息"; exit 1' ERR

# 执行主函数
main "$@"
