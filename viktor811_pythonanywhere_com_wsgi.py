import os
import sys

# Добавляем путь к проекту (используем Working directory)
path = '/home/Viktor811/CooKBooK'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
