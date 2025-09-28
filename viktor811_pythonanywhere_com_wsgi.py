"""
WSGI конфигурация для CookBook проекта на PythonAnywhere.
"""

import os
import sys

# Добавляем путь к проекту в Python path
path = '/home/viktor811/CookBook'
if path not in sys.path:
    sys.path.append(path)

# Устанавливаем переменную окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Импортируем Django WSGI приложение
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()