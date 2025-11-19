# Daily Commands Reference | 日常命令参考

Quick reference for accessing and managing the TCM Clinical System.

---

## Start the System (Daily Use)

### Step 1: Open Terminal
Navigate to the project directory:
```bash
cd C:\Users\User\Documents\GitHub\zhongyi-system\zhongyi_project
```

### Step 2: Activate Virtual Environment
```bash
venv\Scripts\activate
```

### Step 3: Run the Server
```bash
python manage.py runserver
```

### Step 4: Access the System
Open browser and go to:
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/

---

## Quick Start (Copy & Paste)

One-liner to start everything:
```bash
cd C:\Users\User\Documents\GitHub\zhongyi-system\zhongyi_project && venv\Scripts\activate && python manage.py runserver
```

---

## Common Commands

### Database Operations
```bash
# Apply pending migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Create admin/superuser account
python manage.py createsuperuser

# Open database shell
python manage.py dbshell
```

### Development
```bash
# Run tests
python manage.py test

# Open Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic
```

### Translations
```bash
# Compile translation messages
python manage.py compilemessages

# Extract new messages for translation
python manage.py makemessages -l zh_Hans
```

---

## Stop the Server

Press `Ctrl + C` in the terminal where the server is running.

---

## Troubleshooting

### Server won't start
1. Check if virtual environment is activated (you should see `(venv)` in terminal)
2. Run `pip install -r requirements.txt` to ensure dependencies are installed
3. Run `python manage.py migrate` to apply any pending migrations

### Port already in use
Run on a different port:
```bash
python manage.py runserver 8080
```
Then access at http://127.0.0.1:8080/

### Database errors
Reset database (WARNING: deletes all data):
```bash
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## API Endpoints Quick Reference

| Endpoint | Description |
|----------|-------------|
| `/api/users/` | List users |
| `/api/users/me/` | Current user info |
| `/api/patients/` | List/create patients |
| `/api/patients/{id}/` | Patient detail |
| `/api/records/` | Medical records |

---

## Default URLs

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/ | Home page |
| http://127.0.0.1:8000/admin/ | Admin panel |
| http://127.0.0.1:8000/accounts/login/ | Login page |
| http://127.0.0.1:8000/patients/ | Patient list |
| http://127.0.0.1:8000/api/ | API browser |

---

*Last updated: 2025-11-19*
