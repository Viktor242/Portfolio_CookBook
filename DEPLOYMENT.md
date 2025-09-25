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
pip3.10 install --user -r requirements.txt
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
python3.10 manage.py collectstatic
```

### 6. **Создайте суперпользователя**
```bash
python3.10 manage.py createsuperuser
```

### 7. **Настройте Web App**
- **Source code**: `/home/viktor811/CookBook`
- **Working directory**: `/home/viktor811/CookBook`
- **WSGI configuration file**: `/home/viktor811/CookBook/config/wsgi.py`

### 8. **Обновите WSGI файл**
Убедитесь, что в `config/wsgi.py`:
```python
import os
import sys

# Добавьте путь к проекту
path = '/home/viktor811/CookBook'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
```

## 🔧 Возможные проблемы:

### ❌ **ImportError**
- Проверьте, что все зависимости установлены
- Убедитесь, что путь к проекту правильный

### ❌ **Database connection errors**
- Проверьте настройки базы данных
- Убедитесь, что миграции применены

### ❌ **403 Forbidden**
- Проверьте ALLOWED_HOSTS в settings.py
- Убедитесь, что DEBUG=False в продакшне

### ❌ **Static files not found**
- Выполните `collectstatic`
- Проверьте STATIC_ROOT в settings.py

## 📝 Логи для отладки:
- **Error log**: `/home/viktor811/logs/viktor811.pythonanywhere.com.error.log`
- **Server log**: `/home/viktor811/logs/viktor811.pythonanywhere.com.server.log`

## ✅ Проверка работы:
После деплоя проверьте:
1. Главная страница: `https://viktor811.pythonanywhere.com/`
2. Админка: `https://viktor811.pythonanywhere.com/admin/`
3. Статические файлы загружаются
4. Медиа файлы отображаются
