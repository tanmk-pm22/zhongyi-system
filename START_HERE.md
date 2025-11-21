# 🏥 中医临床系统 - 快速启动指南 | Quick Start Guide

欢迎使用中医临床系统！本指南将帮助您快速启动和使用系统。

Welcome to the Zhongyi TCM System! This guide will help you quickly start and use the system.

---

## 📋 系统状态 | System Status

✅ **系统已完成优化和测试**
✅ **System has been optimized and tested**

所有核心功能已验证并正常工作：
- ✅ 数据库连接正常
- ✅ 所有模型测试通过 (10/10)
- ✅ 数据完整性验证通过 (4/4)
- ✅ 处方计算功能正常
- ✅ 服务器可以正常启动

All core features have been verified and are working:
- ✅ Database connection successful
- ✅ All model tests passed (10/10)
- ✅ Data integrity verified (4/4)
- ✅ Prescription calculation working
- ✅ Server starts successfully

---

## 🚀 快速启动 | Quick Start

### 方法一：运行测试后启动 | Method 1: Test then Start

```bash
# 1. 进入项目目录
cd zhongyi_project

# 2. 激活虚拟环境 (Windows)
venv\Scripts\activate

# 3. 运行综合测试
python comprehensive_test.py

# 4. 启动服务器
python manage.py runserver
```

### 方法二：直接启动 | Method 2: Direct Start

```bash
# 1. 进入项目目录
cd zhongyi_project

# 2. 激活虚拟环境并启动
venv\Scripts\activate
python manage.py runserver
```

### 3. 访问系统 | Access the System

打开浏览器访问 | Open your browser and visit:
```
http://localhost:8000
```

或者从局域网其他设备访问 | Or access from other devices on your network:
```
http://YOUR_IP_ADDRESS:8000
```

---

## 👤 登录信息 | Login Information

系统支持三种用户角色 | The system supports three user roles:

1. **管理员 | Administrator**
   - 完全访问权限
   - Full access to all features

2. **执业医师 | Practitioner**
   - 访问分配的患者
   - Access to assigned patients

3. **患者 | Patient**
   - 仅查看自己的记录
   - View own records only

请使用您的账号登录，或联系管理员创建新账号。

Please login with your account, or contact administrator to create a new account.

---

## 📊 系统功能 | System Features

### 1. 患者管理 | Patient Management
- 患者信息登记与管理
- 病历记录
- 诊断历史查看

### 2. 诊断系统 | Diagnosis System
- 四诊采集（望、闻、问、切）
- 症状记录
- 证型辨识
- AI辅助建议

### 3. 处方管理 | Prescription Management
- 中药处方开立
- 中成药处方
- 经典方剂参考
- 价格自动计算

### 4. 数据查询 | Data Query
- 中药数据库
- 中成药数据库
- 经典方剂库
- 症状与证型库

---

## 🔧 系统命令 | System Commands

### 运行测试 | Run Tests
```bash
python comprehensive_test.py
```

### 检查系统 | Check System
```bash
python manage.py check
```

### 查看迁移状态 | Check Migrations
```bash
python manage.py showmigrations
```

### 创建管理员账号 | Create Superuser
```bash
python manage.py createsuperuser
```

### 访问管理后台 | Access Admin Panel
```
http://localhost:8000/admin/
```

---

## 📁 重要文件位置 | Important File Locations

### 配置文件 | Configuration
- 主配置：`zhongyi_project/settings.py`
- URL配置：`zhongyi_project/urls.py`

### 数据库 | Database
- SQLite数据库：`db.sqlite3`

### 模板文件 | Templates
- HTML模板：`templates/`
- 基础模板：`templates/base.html`
- 首页：`templates/home.html`

### 静态文件 | Static Files
- CSS/JS/图片：`static/`

### 测试脚本 | Test Scripts
- 综合测试：`comprehensive_test.py`

---

## 🛠️ 常见问题 | Common Issues

### 问题1：服务器无法启动
**问题 | Issue:** Port already in use

**解决方案 | Solution:**
```bash
# 使用不同端口
python manage.py runserver 8080
```

### 问题2：数据库错误
**问题 | Issue:** Database errors

**解决方案 | Solution:**
```bash
# 运行迁移
python manage.py migrate
```

### 问题3：静态文件不显示
**问题 | Issue:** Static files not loading

**解决方案 | Solution:**
```bash
# 收集静态文件
python manage.py collectstatic
```

### 问题4：编码错误
**问题 | Issue:** Encoding errors in Windows

**解决方案 | Solution:**
确保终端使用UTF-8编码，或使用PowerShell而不是CMD。

Ensure terminal uses UTF-8 encoding, or use PowerShell instead of CMD.

---

## 📚 文档资源 | Documentation

- **项目说明：** `README.md`
- **系统状态：** `SYSTEM_STATUS.md`
- **项目规则：** `CLAUDE.md`
- **日常命令：** `DAILY_COMMANDS.md`

---

## 🎯 下一步做什么？ | What's Next?

1. **启动系统并登录**
   Start the system and login

2. **浏览功能模块**
   Explore feature modules

3. **创建测试数据**
   Create test data if needed

4. **开始使用系统**
   Start using the system

5. **根据需要添加新功能**
   Add new features as needed

---

## 💡 温馨提示 | Tips

1. **双语显示**
   系统所有文字都遵循"中文 | English"格式
   All text follows "Chinese | English" format

2. **数据备份**
   定期备份 `db.sqlite3` 数据库文件
   Regularly backup the `db.sqlite3` database file

3. **开发模式**
   当前为开发模式，生产环境需要额外配置
   Currently in development mode, production requires additional configuration

4. **浏览器兼容**
   推荐使用Chrome、Firefox或Edge最新版本
   Recommended: Latest version of Chrome, Firefox, or Edge

5. **性能优化**
   大量数据时建议切换到PostgreSQL
   For large datasets, consider switching to PostgreSQL

---

## 📞 需要帮助？ | Need Help?

- 查看系统状态报告：`SYSTEM_STATUS.md`
- 运行综合测试检查系统：`python comprehensive_test.py`
- 查看Django日志输出
- 检查浏览器控制台错误

---

**准备好了吗？让我们开始吧！**
**Ready? Let's get started!**

```bash
cd zhongyi_project
venv\Scripts\activate
python manage.py runserver
```

🎉 **系统已准备就绪！| System is ready!**
