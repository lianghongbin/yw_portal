from django.contrib import admin

# Django Admin 只用于系统管理，不包含任何业务模型
# 业务数据管理应通过其他方式进行（API或专门的业务管理界面）
# 
# 系统管理功能包括：
# 1. 用户管理 - Django自带的User和Group（已在Django Admin中自动注册）
# 2. 用户权限管理 - RBAC中的Role、UserRole（在apps/rbac/admin.py中注册）
# 3. 资源权限设置 - RBAC中的Resource、Permission、RolePermission（在apps/rbac/admin.py中注册）