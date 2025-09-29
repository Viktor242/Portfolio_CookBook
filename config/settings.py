from pathlib import Path

# ── Базовая директория ─────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Безопасность ───────────────────────────────────
SECRET_KEY = 'django-insecure-o5_gb=!zu+6!zkyc4^mrr42%t$@!cunee$k9+m3d4k))d6ltnd'

# Определяем продакшн окружение
import os
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'

# Настройки хостов для разных окружений
if DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'viktor811.pythonanywhere.com', 'testserver']
else:
    ALLOWED_HOSTS = ['viktor811.pythonanywhere.com', '127.0.0.1', 'localhost']

# ── Приложения ─────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # наши приложения
    'users',
    'recipes',
    'collections_app',
    'search',
]

# Кастомная модель пользователя
AUTH_USER_MODEL = 'users.User'

# ── Middleware ─────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ── URLs / WSGI ────────────────────────────────────
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ── Шаблоны ────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # глобальные шаблоны
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ── База данных ────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ── Валидаторы паролей ─────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Локализация ────────────────────────────────────
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ── Статика и медиа ────────────────────────────────
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Папка со статическими файлами проекта
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # Для collectstatic

# Медиа файлы (фотографии рецептов, аватары пользователей)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ── Настройки по умолчанию ─────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── Перенаправления при входе/выходе ───────────────
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "users:me"
LOGOUT_REDIRECT_URL = "home"

# ── Настройки сессий ───────────────────────────────
SESSION_COOKIE_AGE = 1209600  # 2 недели
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False