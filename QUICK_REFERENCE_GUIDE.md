# Zhongyi TCM System - Quick Reference Guide
# 中医系统 - 快速参考指南

---

## 📋 Table of Contents | 目录

1. [Export Features | 导出功能](#1-export-features--导出功能)
2. [Print Features | 打印功能](#2-print-features--打印功能)
3. [Patient Portal | 患者门户](#3-patient-portal--患者门户)
4. [URL Reference | URL参考](#4-url-reference--url参考)
5. [Keyboard Shortcuts | 键盘快捷键](#5-keyboard-shortcuts--键盘快捷键)

---

## 1. Export Features | 导出功能

### 1.1 Export Prescription to PDF | 导出处方为PDF

**Steps | 步骤:**
1. Go to: Prescriptions → Select a prescription
2. Click: "导出PDF | Export PDF" button
3. PDF downloads automatically

**URL Pattern:**
```
/prescriptions/{prescription_id}/export-pdf/
```

**Permissions Required:**
- Authenticated user

**Output:**
- Filename: `prescription_{number}.pdf`
- Format: A4 PDF
- Content: Full prescription with herbs, medicines, instructions

---

### 1.2 Export Patient Data to Excel | 导出患者数据为Excel

**Steps | 步骤:**
1. Go to: Patients → Patient List
2. Click: "导出Excel | Export Excel" button (top right)
3. Excel file downloads automatically

**URL Pattern:**
```
/prescriptions/export-patients-excel/
```

**Permissions Required:**
- Admin or Staff only

**Output:**
- Filename: `patients_data_{YYYYMMDD}.xlsx`
- Format: Excel spreadsheet
- Content: All patient information (name, IC, contact, medical history)

---

### 1.3 Export Medical Record to PDF | 导出医疗记录为PDF

**Steps | 步骤:**
1. Go to: Patients → Select Patient → Medical Records → Select Record
2. Click: "导出PDF | Export PDF" button
3. PDF downloads automatically

**URL Pattern:**
```
/prescriptions/medical-record/{record_id}/export-pdf/
```

**Permissions Required:**
- Practitioner (own patients)
- Admin/Staff

**Output:**
- Filename: `medical_record_{IC}_{YYYYMMDD}.pdf`
- Format: A4 PDF
- Content: Complete medical record with four examinations, diagnosis, treatment

---

## 2. Print Features | 打印功能

### 2.1 Print Prescription | 打印处方

**Steps | 步骤:**
1. Go to: Prescriptions → Select a prescription
2. Click: "打印 | Print" button
3. New tab opens with print-friendly view
4. Click print button or press Ctrl+P (Windows) / Cmd+P (Mac)
5. Select printer and settings
6. Click "Print"

**URL Pattern:**
```
/prescriptions/{prescription_id}/print/
```

**Tips | 提示:**
- Use "Save as PDF" to create a PDF file
- Landscape orientation for better fit
- Enable background graphics for colors
- Margins: Normal or Narrow

---

## 3. Patient Portal | 患者门户

### 3.1 Access Patient Portal | 访问患者门户

**Requirements | 要求:**
- Patient account (user with linked patient profile)
- Active patient status

**Steps | 步骤:**
1. Login with patient credentials
2. Navigate to: `/accounts/patient-portal/`
3. View dashboard

**Dashboard Features | 仪表板功能:**
- Personal information
- Statistics (visits, prescriptions, diagnoses)
- Recent activity
- Health tips based on TCM constitution
- Quick links

---

### 3.2 View Prescription History | 查看处方历史

**Steps | 步骤:**
1. Patient Portal → Click "我的处方 | My Prescriptions"
2. OR navigate to: `/accounts/patient-portal/prescriptions/`

**Features | 功能:**
- All prescriptions in card view
- Prescription details (diagnosis, herbs, medicines)
- Decoction method
- Dietary advice
- View details button
- Print button

---

### 3.3 View Appointment History | 查看就诊历史

**Steps | 步骤:**
1. Patient Portal → Click "就诊历史 | Appointment History"
2. OR navigate to: `/accounts/patient-portal/appointments/`

**Features | 功能:**
- Two tabs: Medical Records & Diagnosis Sessions
- Complete visit history
- Chief complaints
- Diagnoses
- Treatment plans
- Next appointment dates

---

### 3.4 Health Tips | 健康建议

**Location:**
- Patient Portal Dashboard (right side)

**Content:**
- Based on your TCM constitution type
- Dietary recommendations
- Exercise guidelines
- Lifestyle advice
- Prevention measures

**Constitution Types Supported:**
- 气虚质 (Qi Deficiency)
- 阳虚质 (Yang Deficiency)
- 阴虚质 (Yin Deficiency)
- 痰湿质 (Phlegm-Dampness)
- 湿热质 (Damp-Heat)
- 血瘀质 (Blood Stasis)
- 气郁质 (Qi Stagnation)
- 特禀质 (Special Constitution)
- 平和质 (Balanced Constitution)

---

## 4. URL Reference | URL参考

### Main URLs | 主要URL

```
# Dashboard
/accounts/dashboard/                  - Main dashboard

# Patients
/patients/                           - Patient list
/patients/create/                    - Create patient
/patients/{id}/                      - Patient detail

# Prescriptions
/prescriptions/                      - Prescription list
/prescriptions/create/               - Select patient for prescription
/prescriptions/create/{patient_id}/  - Create prescription
/prescriptions/{id}/                 - Prescription detail
/prescriptions/{id}/print/           - Print prescription
/prescriptions/{id}/export-pdf/      - Export prescription PDF

# Export
/prescriptions/export-patients-excel/         - Export all patients to Excel
/prescriptions/medical-record/{id}/export-pdf/ - Export medical record PDF

# Patient Portal
/accounts/patient-portal/                    - Patient dashboard
/accounts/patient-portal/prescriptions/      - Patient prescription history
/accounts/patient-portal/appointments/       - Patient appointment history

# Medicine Library
/prescriptions/herbs/                - Herb list
/prescriptions/formulas/             - Classic formula list
/prescriptions/patent-medicines/     - Patent medicine list

# Diagnosis
/diagnosis/                          - Diagnosis list
/diagnosis/create/                   - Select patient for diagnosis
/diagnosis/create/{patient_id}/      - Create diagnosis
```

---

## 5. Keyboard Shortcuts | 键盘快捷键

### Global Shortcuts | 全局快捷键

```
Ctrl+P (Windows) / Cmd+P (Mac)  - Print current page
Ctrl+S (Windows) / Cmd+S (Mac)  - Save (in forms)
Ctrl+F (Windows) / Cmd+F (Mac)  - Find in page
Esc                              - Close modals/dialogs
```

### Navigation Shortcuts | 导航快捷键

```
Alt+H          - Home/Dashboard
Alt+P          - Patients
Alt+R          - Prescriptions
Alt+D          - Diagnosis
```

*(Note: These shortcuts may vary by browser)*

---

## 6. Common Tasks | 常见任务

### Task 1: Create New Prescription | 创建新处方

```
1. Prescriptions → "新建处方 | New Prescription"
2. Select patient from list
3. Fill in diagnosis and treatment principle
4. Add herbs (search and select)
5. Add patent medicines (optional)
6. Set doses (default: 7)
7. Add decoction method
8. Add dietary/lifestyle advice
9. Click "保存 | Save"
```

### Task 2: Print Prescription for Patient | 为患者打印处方

```
1. Prescriptions → Select prescription
2. Click "打印 | Print"
3. Review print preview
4. Press Ctrl+P or click print button
5. Select printer
6. Print
```

### Task 3: Export Patient Data for Analysis | 导出患者数据进行分析

```
1. Login as admin/staff
2. Go to Patients list
3. Click "导出Excel | Export Excel"
4. Open in Excel/LibreOffice
5. Analyze data
```

### Task 4: Check Patient Portal as Patient | 作为患者查看门户

```
1. Login with patient account
2. Navigate to Patient Portal
3. View statistics and recent activity
4. Check prescriptions
5. Review health tips
6. View appointment history
```

---

## 7. Troubleshooting | 故障排除

### Issue: PDF/Excel not downloading | PDF/Excel未下载

**Solution:**
1. Check browser pop-up blocker
2. Allow downloads from this site
3. Try different browser
4. Check internet connection

### Issue: Print button not working | 打印按钮不起作用

**Solution:**
1. Make sure new tab opened
2. Try Ctrl+P directly
3. Check browser print settings
4. Update browser

### Issue: Patient portal not accessible | 患者门户无法访问

**Solution:**
1. Verify you have patient profile linked
2. Check with admin to link account
3. Ensure patient status is active
4. Clear browser cache and cookies

### Issue: Chinese characters not showing in PDF | PDF中文字符未显示

**Solution:**
1. System automatically uses available fonts
2. On Linux servers, install Chinese fonts:
   ```bash
   sudo apt-get install fonts-wqy-microhei
   ```
3. Contact system administrator

### Issue: Export button not visible | 导出按钮不可见

**Solution:**
1. Check your user role/permissions
2. Excel export: Admin/Staff only
3. PDF export: Available to all authenticated users
4. Contact admin for permission upgrade

---

## 8. Best Practices | 最佳实践

### For Practitioners | 给医师的建议:

1. ✅ Always review prescription before printing
2. ✅ Include dietary and lifestyle advice
3. ✅ Use clear, specific diagnoses
4. ✅ Verify patient information before prescribing
5. ✅ Keep detailed medical records

### For Admins | 给管理员的建议:

1. ✅ Regular patient data backups (use Excel export)
2. ✅ Monitor system usage and performance
3. ✅ Keep user permissions up to date
4. ✅ Review and update herb database regularly
5. ✅ Train staff on new features

### For Patients | 给患者的建议:

1. ✅ Check patient portal regularly
2. ✅ Read health tips for your constitution
3. ✅ Follow prescribed treatment plans
4. ✅ Keep track of appointment history
5. ✅ Contact practitioner with questions

---

## 9. Support | 支持

### Getting Help | 获取帮助:

**For Technical Issues:**
- Contact system administrator
- Email: admin@zhongyi-clinic.com (example)

**For Medical Questions:**
- Contact your assigned practitioner
- Book appointment through clinic

**For Account Issues:**
- Contact clinic reception
- Request password reset
- Update personal information

---

## 10. System Information | 系统信息

**Version:** 2.0
**Last Updated:** 2025-11-23
**Framework:** Django 4.2+
**UI Framework:** Bootstrap 5
**Supported Browsers:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

**End of Quick Reference Guide**
**快速参考指南结束**

Keep this guide handy for quick reference!
请保存此指南以便快速查阅！
