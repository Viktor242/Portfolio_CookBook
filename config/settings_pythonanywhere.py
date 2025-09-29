# config/settings_pythonanywhere.py
from .settings import *
import os

# Переопределяем настройки для PythonAnywhere
DEBUG = False
ALLOWED_HOSTS = ['Viktor811.pythonanywhere.com', '127.0.0.1', 'localhost']

# Настройки статических файлов для PythonAnywhere
STATIC_URL = '/static/'
STATIC_ROOT = '/home/Viktor811/CookBook/staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/Viktor811/CookBook/media'

# Настройки базы данных для PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/Viktor811/CookBook/db.sqlite3',
    }
}

# Настройки безопасности для PythonAnywhere
SECURE_SSL_REDIRECT = False  # PythonAnywhere использует HTTPS на своем уровне
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Настройки логирования для отладки
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/Viktor811/CookBook/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Настройки для работы с файлами
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
