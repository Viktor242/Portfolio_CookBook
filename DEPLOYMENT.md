# 🚀 Инструкция по деплою на PythonAnywhere

## 📋 Шаги для деплоя:

### 1. **Загрузите код на PythonAnywhere**
```bash
# Клонируйте репозиторий в консоли PythonAnywhere
git clone https://github.com/Viktor242/CookBook.git
cd CookBook
```

### 2. **Установите зависимости**
```bash
python3.10 -m pip install --user -r requirements.txt
```

### 3. **Настройте переменные окружения**
В консоли PythonAnywhere:
```bash
export DJANGO_DEBUG=False
```

### 4. **Примените миграции**
```bash
python3.10 manage.py migrate
```

### 5. **Соберите статические файлы**
```bash
python3.10 manage.py collectstatic --noinput
```

### 6. **Создайте суперпользователя**
```bash
python3.10 manage.py createsuperuser
```

### 7. **Настройте права доступа**
```bash
chmod -R 755 /home/Viktor811/CookBook/
```

### 8. **Настройте Web App в панели PythonAnywhere**
- **Source code**: `/home/Viktor811/CookBook`
- **Working directory**: `/home/Viktor811/CookBook`
- **WSGI configuration file**: `/var/www/viktor811_pythonanywhere_com_wsgi.py`

### 9. **Настройте статические файлы в панели PythonAnywhere**
- **URL**: `/static/`
- **Directory**: `/home/Viktor811/CookBook/staticfiles`

### 10. **Настройте медиа файлы в панели PythonAnywhere**
- **URL**: `/media/`
- **Directory**: `/home/Viktor811/CookBook/media`

### 11. **Обновите WSGI файл**
Создайте файл `/var/www/viktor811_pythonanywhere_com_wsgi.py`:
```python
import os
import sys

# Добавляем путь к проекту
path = '/home/Viktor811/CookBook'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
```

## 🔧 Возможные проблемы и решения:

### ❌ **NameError: name 'BASE_DIR' is not defined**
**Решение:**
```bash
# Проверьте, что в config/settings.py есть:
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
```

### ❌ **ModuleNotFoundError: No module named 'recipes.models'**
**Решение:**
```bash
# Убедитесь, что WSGI файл правильно настроен
# Проверьте, что путь к проекту добавлен в sys.path
```

### ❌ **DisallowedHost: Invalid HTTP_HOST header**
**Решение:**
```bash
# В config/settings.py добавьте:
ALLOWED_HOSTS = ['viktor811.pythonanywhere.com', '127.0.0.1', 'localhost']
```

### ❌ **Static files not found (404)**
**Решение:**
```bash
# 1. Соберите статические файлы:
python3.10 manage.py collectstatic --noinput

# 2. Проверьте настройки в панели PythonAnywhere:
# URL: /static/
# Directory: /home/Viktor811/CookBook/staticfiles

# 3. Проверьте права доступа:
chmod -R 755 /home/Viktor811/CookBook/staticfiles/
```

### ❌ **ImportError**
**Решение:**
```bash
# Установите зависимости:
python3.10 -m pip install --user -r requirements.txt

# Проверьте, что путь к проекту правильный в WSGI файле
```

### ❌ **Database connection errors**
**Решение:**
```bash
# Примените миграции:
python3.10 manage.py migrate

# Создайте суперпользователя:
python3.10 manage.py createsuperuser
```

### ❌ **403 Forbidden**
**Решение:**
```bash
# Проверьте ALLOWED_HOSTS в config/settings.py
# Убедитесь, что DEBUG=False в продакшне
```

## 📝 Логи для отладки:
- **Error log**: `/home/Viktor811/logs/viktor811.pythonanywhere.com.error.log`
- **Server log**: `/home/Viktor811/logs/viktor811.pythonanywhere.com.server.log`

## 🔍 Команды для диагностики:
```bash
# Проверка структуры проекта:
ls -la /home/Viktor811/CookBook/

# Проверка статических файлов:
ls -la /home/Viktor811/CookBook/staticfiles/

# Проверка медиа файлов:
ls -la /home/Viktor811/CookBook/media/

# Проверка WSGI файла:
cat /var/www/viktor811_pythonanywhere_com_wsgi.py

# Проверка настроек Django:
python3.10 manage.py check
```

## ✅ Проверка работы:
После деплоя проверьте:
1. **Главная страница**: `https://viktor811.pythonanywhere.com/`
2. **Админка**: `https://viktor811.pythonanywhere.com/admin/`
3. **Статические файлы**: `https://viktor811.pythonanywhere.com/static/css/main.css`
4. **Медиа файлы**: `https://viktor811.pythonanywhere.com/media/`
5. **Форма добавления рецепта**: `https://viktor811.pythonanywhere.com/recipes/create/`

## 🚨 Важные замечания:
- **Всегда используйте правильный регистр** в путях (`Viktor811` vs `viktor811`)
- **Перезапускайте Web App** после изменений в настройках
- **Проверяйте логи** при возникновении ошибок
- **Используйте `--noinput`** для автоматических команд
