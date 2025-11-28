# Quick Start Guide | 快速启动指南
# Zhongyi TCM System - Enhanced Version

**Version:** 2.0 Enhanced
**Date:** 2025-11-22

---

## Step-by-Step Setup | 分步设置指南

### Step 1: Activate Virtual Environment | 激活虚拟环境

**Windows:**
```bash
cd C:\Users\User\Documents\GitHub\zhongyi-system\zhongyi_project
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd /path/to/zhongyi-system/zhongyi_project
source venv/bin/activate
```

You should see `(venv)` in your command prompt.

---

### Step 2: Install Required Packages (Optional) | 安装所需包（可选）

The core dependencies should already be installed. If you need export functionality:

```bash
pip install reportlab openpyxl
```

---

### Step 3: Create Database Migrations | 创建数据库迁移

Run the following commands to create migrations for all new modules:

```bash
python manage.py makemigrations patients
python manage.py makemigrations constitution
python manage.py makemigrations cupping
python manage.py makemigrations tuina
python manage.py makemigrations treatment_course
python manage.py makemigrations appointments
python manage.py makemigrations prescriptions
```

**Expected Output:**
```
Migrations for 'patients':
  patients\migrations\0002_medicalhistorytimeline.py
    - Create model MedicalHistoryTimeline
...
```

---

### Step 4: Apply Migrations to Database | 应用迁移到数据库

```bash
python manage.py migrate
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Applying patients.0002_medicalhistorytimeline... OK
  Applying constitution.0001_initial... OK
  Applying cupping.0001_initial... OK
  Applying tuina.0001_initial... OK
  Applying treatment_course.0001_initial... OK
  Applying appointments.0001_initial... OK
  Applying prescriptions.0002_auto... OK
```

---

### Step 5: Create Superuser (if needed) | 创建超级用户（如需要）

If you don't have an admin user yet:

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

---

### Step 6: Run Test Script | 运行测试脚本

This will verify all modules are working and create sample data:

```bash
python comprehensive_system_test.py
```

**Expected Output:**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        增强版中医系统综合测试                                ║
║              Zhongyi TCM System - Comprehensive Test Suite                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

开始时间 | Start Time: 2025-11-22 23:30:00

================================================================================
  测试 1: 患者病史时间线 | Test 1: Patient Medical History Timeline
================================================================================
  ✓ Found patient: John Doe
  ✓ Created timeline event: 首次诊断 | Initial Diagnosis
  ✓ Patient has 1 timeline event(s)
  ✅ Patient History Timeline: PASSED

...

================================================================================
  测试总结 | Test Summary
================================================================================

  测试结果 | Test Results:
    ✅ PASSED - 患者病史时间线 | Patient History Timeline
    ✅ PASSED - 体质辨识模块 | Constitution Analysis
    ✅ PASSED - 拔罐治疗模块 | Cupping Therapy
    ✅ PASSED - 推拿治疗模块 | Tuina/Massage
    ✅ PASSED - 疗程管理模块 | Treatment Course
    ✅ PASSED - 预约管理系统 | Appointment System
    ✅ PASSED - 处方模板和煎药 | Prescription Enhancements

  总计 | Total: 7/7 tests passed
  成功率 | Success Rate: 100.0%

  🎉 所有测试通过！| All tests passed!
  ✅ 系统功能正常 | System is functioning correctly
```

---

### Step 7: Start Development Server | 启动开发服务器

```bash
python manage.py runserver
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 22, 2025 - 23:30:00
Django version 4.2.x, using settings 'zhongyi_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### Step 8: Access the System | 访问系统

Open your web browser and navigate to:

**Admin Interface:**
```
http://127.0.0.1:8000/admin/
```

Login with your superuser credentials.

**Main Application:**
```
http://127.0.0.1:8000/
```

---

## What's New in This Version? | 新版本功能

### 🆕 New Modules | 新模块

1. **Constitution Analysis (体质辨识)**
   - `/admin/constitution/` - Manage 9 constitution types
   - `/constitution/` - Constitution assessment interface

2. **Cupping Therapy (拔罐治疗)**
   - `/admin/cupping/` - Cupping techniques and sessions
   - `/cupping/` - Cupping treatment records

3. **Tuina/Massage (推拿治疗)**
   - `/admin/tuina/` - Tuina techniques and sessions
   - `/tuina/` - Tuina treatment records

4. **Treatment Courses (疗程管理)**
   - `/admin/treatment_course/` - Course management
   - `/treatment-course/` - Course tracking

5. **Appointments (预约系统)**
   - `/admin/appointments/` - Appointment management
   - `/appointments/` - Appointment scheduling
   - `/appointments/calendar/` - Calendar view

### ✨ Enhanced Modules | 增强模块

1. **Patient Management**
   - Medical History Timeline tracking
   - Comprehensive event logging

2. **Prescriptions**
   - Decoction Methods library
   - Prescription Templates
   - Quick prescription creation

---

## Admin Interface Navigation | 管理界面导航

After logging into `/admin/`, you'll see these sections:

### 患者管理 | PATIENTS
- Patients (患者)
- Medical Records (医疗记录)
- Medical History Timeline (病史时间线) 🆕

### 体质辨识 | CONSTITUTION ANALYSIS 🆕
- Constitution Types (体质类型)
- Constitution Questionnaires (体质问卷)
- Constitution Assessments (体质评估)
- Assessment Answers (问卷答案)

### 拔罐治疗 | CUPPING THERAPY 🆕
- Cupping Techniques (拔罐手法)
- Cupping Sessions (拔罐记录)
- Session Techniques (治疗手法记录)

### 推拿治疗 | TUINA THERAPY 🆕
- Tuina Techniques (推拿手法)
- Tuina Sessions (推拿记录)
- Session Techniques (治疗手法记录)

### 疗程管理 | TREATMENT COURSE MANAGEMENT 🆕
- Treatment Courses (治疗疗程)
- Course Sessions (疗程治疗记录)

### 预约管理 | APPOINTMENT MANAGEMENT 🆕
- Appointment Types (预约类型)
- Practitioner Schedules (医师排班)
- Appointments (预约)

### 处方系统 | PRESCRIPTIONS
- Herbs (中药)
- Classic Formulas (经典方剂)
- Prescriptions (处方)
- Patent Medicines (中成药)
- Decoction Methods (煎药方法) 🆕
- Prescription Templates (处方模板) 🆕

---

## Common Tasks | 常见任务

### Create a Constitution Assessment | 创建体质评估

1. Go to `/admin/constitution/constitutionassessment/`
2. Click "Add Constitution Assessment"
3. Select patient and practitioner
4. Choose primary constitution type
5. Enter scores
6. Add AI analysis and recommendations
7. Save

### Create a Treatment Course | 创建治疗疗程

1. Go to `/admin/treatment_course/treatmentcourse/`
2. Click "Add Treatment Course"
3. Select patient and practitioner
4. Enter course details (name, diagnosis, treatment plan)
5. Set planned sessions and frequency
6. Check treatment modalities to include
7. Save and add individual sessions

### Schedule an Appointment | 预约排期

1. Go to `/admin/appointments/appointment/`
2. Click "Add Appointment"
3. Select patient, practitioner, and appointment type
4. Choose date and time
5. Enter reason for visit
6. Set status (pending/confirmed)
7. Save

### Create Prescription from Template | 从模板创建处方

1. Go to `/admin/prescriptions/prescriptiontemplate/`
2. Browse available templates
3. Use template to create new prescription
4. Modify herbs as needed
5. Add decoction instructions

---

## Troubleshooting | 故障排除

### Issue: Migration Errors | 问题：迁移错误

**Solution:**
```bash
# Delete migration files (keep __init__.py)
# Then recreate:
python manage.py makemigrations
python manage.py migrate
```

### Issue: Import Errors | 问题：导入错误

**Solution:**
```bash
# Make sure virtual environment is activated
# Check PYTHONPATH
python -c "import django; print(django.__version__)"
```

### Issue: Port Already in Use | 问题：端口已被占用

**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or kill existing process on Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Static Files Not Loading | 问题：静态文件未加载

**Solution:**
```bash
python manage.py collectstatic
```

---

## Data Population Tips | 数据填充提示

### Create Sample Constitution Types | 创建样本体质类型

The test script creates basic data. For complete data:

1. Go to `/admin/constitution/constitutiontype/`
2. Add all 9 constitution types with detailed descriptions
3. Add questionnaire items for each type

### Create Sample Techniques | 创建样本手法

1. **Cupping:** Add common techniques (留罐, 闪罐, 走罐)
2. **Tuina:** Add basic manipulations (推法, 拿法, 按法)

### Create Practitioner Schedules | 创建医师排班

1. Go to `/admin/appointments/practitionerschedule/`
2. For each practitioner, add weekly schedule
3. Set working hours and time slot duration

---

## Next Steps | 下一步

After setup, you can:

1. **Add Real Patient Data** - Start entering actual patient records
2. **Customize Constitution Questions** - Tailor questionnaires to your practice
3. **Create Prescription Templates** - Build library of common formulas
4. **Set Up Practitioner Schedules** - Configure appointment availability
5. **Train Staff** - Familiarize team with new modules
6. **Configure Settings** - Adjust system to your clinic's needs

---

## Resources | 资源

**Documentation:**
- `IMPLEMENTATION_SUMMARY.md` - Complete feature documentation
- `CLAUDE.md` - Coding guidelines and best practices
- `comprehensive_system_test.py` - Test and sample data script

**Key Commands:**
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python comprehensive_system_test.py

# Start server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell
```

---

## Support | 技术支持

For issues or questions:

1. Check `IMPLEMENTATION_SUMMARY.md` for detailed documentation
2. Review model definitions in `*/models.py` files
3. Examine admin configurations in `*/admin.py` files
4. Run test script to verify system status

---

## Success Checklist | 成功检查清单

- [ ] Virtual environment activated
- [ ] All migrations created and applied
- [ ] Superuser account created
- [ ] Test script runs successfully (7/7 tests passed)
- [ ] Development server starts without errors
- [ ] Can access admin interface
- [ ] All new modules visible in admin
- [ ] Sample data created

---

**System Ready! | 系统就绪！** ✅

You're now ready to use the enhanced Zhongyi TCM System with all new features!

现在可以使用增强版中医系统的所有新功能了！

---

**Version:** 2.0 Enhanced
**Last Updated:** 2025-11-22
