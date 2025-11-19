# TCM Clinical System | 中医临床系统

AI-Enhanced Traditional Chinese Medicine Clinical System for Malaysia, compliant with T&CM Act 2016 and PDPA 2010.

## Features

- **Patient Management** - Comprehensive patient records with QR code identification
- **Medical Records** - TCM diagnosis documentation with Four Examinations (四诊)
- **User Roles** - Administrator, Practitioner, and Patient roles
- **REST API** - Full API with Django REST Framework
- **Bilingual** - English and Chinese (Simplified) interface
- **PDPA Compliant** - Data consent tracking for Malaysia's privacy regulations

## Quick Start

### 1. Set up Virtual Environment

```bash
# Navigate to the project directory
cd zhongyi_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
# Create migrations
python manage.py makemigrations accounts
python manage.py makemigrations patients

# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
```

### 4. Compile Translations (Optional)

```bash
python manage.py compilemessages
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## Project Structure

```
zhongyi_project/
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── db.sqlite3             # SQLite database (created after migrate)
│
├── zhongyi_project/       # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI entry point
│
├── accounts/              # User authentication app
│   ├── models.py          # Custom User model with roles
│   ├── views.py           # Auth views (login, register, profile)
│   ├── forms.py           # User forms
│   └── urls.py            # Auth URL patterns
│
├── patients/              # Patient management app
│   ├── models.py          # Patient and MedicalRecord models
│   ├── views.py           # Patient CRUD views
│   ├── forms.py           # Patient forms
│   └── urls.py            # Patient URL patterns
│
├── api/                   # REST API app
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API viewsets
│   └── urls.py            # API URL patterns
│
├── templates/             # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── home.html          # Home page
│   ├── accounts/          # Auth templates
│   └── patients/          # Patient templates
│
├── static/                # Static files
│   └── css/
│       └── style.css      # Custom styles
│
└── locale/                # Translation files
    ├── en/
    └── zh_Hans/
```

## User Roles

| Role | Access |
|------|--------|
| **Admin** | Full system access, user management |
| **Practitioner** | Patient management, medical records |
| **Patient** | View own records (future feature) |

## API Endpoints

The REST API is available at `/api/`:

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/users/` | GET | List users |
| `/api/users/me/` | GET | Current user info |
| `/api/users/practitioners/` | GET | List practitioners |
| `/api/patients/` | GET, POST | List/create patients |
| `/api/patients/{id}/` | GET, PUT, DELETE | Patient detail |
| `/api/patients/{id}/records/` | GET | Patient's medical records |
| `/api/patients/search/` | GET | Search patients |
| `/api/records/` | GET, POST | List/create medical records |
| `/api/records/{id}/` | GET, PUT, DELETE | Record detail |

## Development

### Create New Translations

```bash
# Extract messages
python manage.py makemessages -l zh_Hans

# Compile after editing .po files
python manage.py compilemessages
```

### Run Tests

```bash
python manage.py test
```

### Production Deployment

1. Set `DEBUG = False` in settings.py
2. Generate new `SECRET_KEY`
3. Configure proper database (PostgreSQL recommended)
4. Set up static file serving
5. Configure HTTPS

## License

Copyright © 2024. All rights reserved.

## Compliance

This system is designed to be compliant with:
- Malaysia Traditional & Complementary Medicine Act 2016
- Malaysia Personal Data Protection Act 2010 (PDPA)
