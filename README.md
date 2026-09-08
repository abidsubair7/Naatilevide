# Naatilevide

Django + MySQL community platform for Kerala stories, places and events.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Deployment

GitHub stores the source code; it does not execute the Django backend. The project includes `render.yaml` and `Procfile` for deployment on a Python-capable host such as Render.

Set these environment variables on the host:

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`

Never commit `.env`, database passwords, or production secrets. The `.gitignore` excludes `.env`, virtual environments, and generated media/staticfiles.

## Authentication

Authentication uses Django's built-in session authentication, not JWT. Registration uses `UserCreationForm`; login calls `authenticate()` and then `login()`. Protected views use `@login_required`. Django sessions are maintained by `SessionMiddleware` and the authenticated user is exposed through `AuthenticationMiddleware`.
