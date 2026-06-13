# The Wardrobe Door — Django E-Commerce

Full-stack clothing e-commerce built with **Django**, **PostgreSQL/SQLite**, **django-allauth**, and **Mailtrap**. Custom black/red responsive UI theme.

## Features

- User registration, login, password reset (django-allauth)
- Welcome & order confirmation emails (Mailtrap SMTP)
- Product catalog with category filters
- Session shopping cart with AJAX add-to-cart
- Checkout with shipping address stored on orders
- Admin panel (products, orders, users)
- Original responsive CSS theme (Playfair Display + Font Awesome)

## Quick Start

### 1. Create virtual environment

```bash
cd "Wardrobe Doorr"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
copy .env.example .env
```

Edit `.env` — see [Environment variables](#environment-variables) below.

### 3. Database & demo data

```bash
python manage.py migrate
python manage.py setup_demo
```

### 4. Run the server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/**

**Demo admin login:** `admin` / `admin123`

## Environment variables

Create a `.env` file in the project root (copy from `.env.example`):

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | `django-insecure-abc123...` | Random secret key. Generate one for production. |
| `DEBUG` | Yes | `True` | `False` in production |
| `ALLOWED_HOSTS` | Yes | `localhost,127.0.0.1` | Comma-separated domains |
| `SITE_NAME` | No | `The Wardrobe Door` | Shown in header/footer |
| `DB_ENGINE` | Yes | `sqlite` | `sqlite` for local dev, `postgresql` for production |
| `DB_NAME` | If PostgreSQL | `wardrobe_door` | Database name |
| `DB_USER` | If PostgreSQL | `postgres` | Database user |
| `DB_PASSWORD` | If PostgreSQL | `yourpassword` | Database password |
| `DB_HOST` | If PostgreSQL | `localhost` | Database host |
| `DB_PORT` | If PostgreSQL | `5432` | Database port |
| `EMAIL_BACKEND` | Yes | `django.core.mail.backends.smtp.EmailBackend` | Use SMTP for Mailtrap |
| `EMAIL_HOST` | Yes | `sandbox.smtp.mailtrap.io` | Mailtrap SMTP host |
| `EMAIL_PORT` | Yes | `2525` | Mailtrap SMTP port |
| `EMAIL_HOST_USER` | Yes | *(from Mailtrap)* | Mailtrap SMTP username |
| `EMAIL_HOST_PASSWORD` | Yes | *(from Mailtrap)* | Mailtrap SMTP password |
| `EMAIL_USE_TLS` | Yes | `True` | Enable TLS |
| `DEFAULT_FROM_EMAIL` | Yes | `The Wardrobe Door <noreply@wardrobe-door.com>` | Sender address |
| `ACCOUNT_EMAIL_VERIFICATION` | No | `optional` | `optional`, `mandatory`, or `none` |
| `CSRF_TRUSTED_ORIGINS` | Production | `https://your-app.onrender.com` | Your live URL |

### Mailtrap setup

1. Sign up at [mailtrap.io](https://mailtrap.io)
2. Go to **Email Testing → Inboxes → SMTP Settings**
3. Copy **Username** → `EMAIL_HOST_USER`
4. Copy **Password** → `EMAIL_HOST_PASSWORD`

Emails captured in Mailtrap: welcome on register, password reset, order confirmation.

### Example `.env` for local development

```env
SECRET_KEY=your-long-random-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SITE_NAME=The Wardrobe Door

DB_ENGINE=sqlite

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=sandbox.smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=your_mailtrap_username
EMAIL_HOST_PASSWORD=your_mailtrap_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=The Wardrobe Door <noreply@wardrobe-door.com>

ACCOUNT_EMAIL_VERIFICATION=optional
```

## Project structure

```
config/           # Django settings & URLs
catalog/          # Products, home, product pages
shopping_cart/    # Cart & checkout
orders/           # Orders & confirmation emails
panel/            # Custom admin dashboard
templates/        # HTML templates
static/           # CSS, JS, images
media/            # Uploaded product images
```

## Deploy (Render / Railway)

1. Push code to GitHub
2. Connect repo to Render or Railway
3. Set all `.env` variables on the host
4. Set `DB_ENGINE=postgresql` and PostgreSQL credentials
5. Set `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`
6. Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
7. Start: `gunicorn config.wsgi`

## Default credentials

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | admin    | admin123  |
