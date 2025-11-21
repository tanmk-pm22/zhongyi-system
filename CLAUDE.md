# Zhongyi TCM System - Project Instructions

## MANDATORY RULES

**You MUST follow these rules for ALL code, templates, and content in this project.**

### Rule 1: Bilingual Display (双语显示) - MOST IMPORTANT

ALL user-facing text MUST be bilingual with **Chinese FIRST, English second**.

**Format:** `中文 | English`

Examples:
- Titles: `处方管理 | Prescriptions`
- Buttons: `保存 | Save`
- Table headers: `患者 | Patient`
- Form labels: `诊断 | Diagnosis`
- Messages: `处方已创建！| Prescription created successfully!`
- Model verbose_name: `_('名称 | Name')`

**NEVER write English-only or English-first text in templates!**

### Rule 2: Project Structure

```
zhongyi_project/
├── accounts/       # User authentication
├── patients/       # Patient management
├── diagnosis/      # TCM diagnosis (四诊)
├── prescriptions/  # Herbal prescriptions
├── api/            # REST API
├── templates/      # HTML templates
└── static/         # CSS, JS
```

### Rule 3: Required Model Fields

Every model must include:
- `created_at` - auto_now_add=True
- `updated_at` - auto_now=True
- `is_active` - for soft delete

### Rule 4: User Roles

- `admin` - Full access
- `practitioner` - Access to assigned patients
- `patient` - Own records only

### Rule 5: Technology Stack

- Django 4.2+
- Django REST Framework
- Bootstrap 5
- Bootstrap Icons
- SQLite (dev) / PostgreSQL (prod)

## Common Bilingual Phrases

| Chinese | English | Format |
|---------|---------|--------|
| 新建 | New | 新建 \| New |
| 编辑 | Edit | 编辑 \| Edit |
| 删除 | Delete | 删除 \| Delete |
| 保存 | Save | 保存 \| Save |
| 取消 | Cancel | 取消 \| Cancel |
| 返回 | Back | 返回 \| Back |
| 患者 | Patient | 患者 \| Patient |
| 医师 | Practitioner | 医师 \| Practitioner |
| 诊断 | Diagnosis | 诊断 \| Diagnosis |
| 处方 | Prescription | 处方 \| Prescription |

## Additional Rules

For complete rules and examples, see: `.claude/skills/zhongyi-rules/SKILL.md`

## Quick Checklist

Before writing any code:
- [ ] All text is bilingual (中文 | English)
- [ ] Chinese comes FIRST
- [ ] Using Bootstrap 5 classes
- [ ] Using Bootstrap Icons
- [ ] Models have required fields
- [ ] Views check user permissions
