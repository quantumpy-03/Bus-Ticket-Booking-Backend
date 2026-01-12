# Bus Ticket Booking — Backend

Small Django backend for a bus ticket booking app (REST API).

## Overview
- Django REST Framework backend with JWT auth (`djangorestframework-simplejwt`).
- Uses `dj-database-url` to parse `DATABASE_URL` from `.env`.
- Static files served via WhiteNoise for simple deployments.
- Management commands to import sample data: `add_sample_routes`, `add_sample_buses`.

## Requirements
- Python 3.10+ (see `.env` for desired version)
- PostgreSQL (recommended) or SQLite for local development
- Install dependencies:

```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows PowerShell
pip install -r requirements.txt
```

## Environment
Place a `.env` file at the project root (backend/) with the following variables:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=yourdomain.com,localhost,127.0.0.1
DATABASE_URL= your_database
RAZORPAY_KEY_ID=...
RAZORPAY_SECRET_KEY=...
CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000
```

Notes:
- In `settings.py` `CORS_ALLOWED_ORIGINS` values are sanitized to strip trailing slashes. Do not include paths in origins (no trailing `/path`).
- Ensure `DEBUG=False` in production.

## Setup & Run (development)
```bash
# Create DB migrations and apply
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Optional: import sample data
python manage.py add_sample_routes
python manage.py add_sample_buses

# Run local server
python manage.py runserver
```

## Management commands
- `python manage.py add_sample_routes` — adds a set of sample `Route` rows.
- `python manage.py add_sample_buses` — adds sample `Bus` rows and attaches routes when available.

## Admin
- Admin customizations live in `app/admin.py`. If you change model field names, update admin list/filter/search fields accordingly.

## Database migrations notes
- When adding non-nullable fields to existing models, either:
  - Add the field as `null=True` first, migrate, populate values, then make it non-nullable; or
  - Provide a one-off default during `makemigrations` (not recommended for unique fields).

## Deployment tips
- Run `collectstatic` and use a WSGI server (Gunicorn) behind a reverse proxy in production.
- Set `DEBUG=False` and configure `ALLOWED_HOSTS` correctly.
- Use a secure secrets store (do not commit `.env` to VCS).

## Troubleshooting
- If you see CORS errors, verify `CORS_ALLOWED_ORIGINS` entries contain no path component and no trailing slash.
- If Django system checks show admin field errors after renaming model fields, update `app/admin.py` to reference new field names.

## Contributing / Next steps
- Add serializers/views for buses, routes, bookings.
- Add API tests and CI pipeline.

----
If you want, I can also add a short `run-local.sh` or `Procfile` example for deployment. Let me know.