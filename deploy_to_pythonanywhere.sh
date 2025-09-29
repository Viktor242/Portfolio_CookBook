#!/bin/bash
# deploy_to_pythonanywhere.sh
# Скрипт для автоматического деплоя проекта на PythonAnywhere

echo "🚀 Начинаем деплой проекта CookBook на PythonAnywhere..."

# Переменные
PROJECT_NAME="CookBook"
PYTHONANYWHERE_USER="Viktor811"
PYTHONANYWHERE_PATH="/home/$PYTHONANYWHERE_USER/$PROJECT_NAME"

echo "📁 Путь к проекту: $PYTHONANYWHERE_PATH"

# 1. Создание директорий
echo "📂 Создаем необходимые директории..."
mkdir -p $PYTHONANYWHERE_PATH/staticfiles
mkdir -p $PYTHONANYWHERE_PATH/media
mkdir -p $PYTHONANYWHERE_PATH/logs

# 2. Копирование файлов проекта
echo "📋 Копируем файлы проекта..."
cp -r . $PYTHONANYWHERE_PATH/

# 3. Установка зависимостей
echo "📦 Устанавливаем зависимости..."
cd $PYTHONANYWHERE_PATH
pip3.10 install --user -r requirements_pythonanywhere.txt

# 4. Настройка базы данных
echo "🗄️ Настраиваем базу данных..."
python3.10 manage.py migrate

# 5. Сбор статических файлов
echo "📁 Собираем статические файлы..."
python3.10 manage.py collectstatic --noinput

# 6. Создание суперпользователя (если нужно)
echo "👤 Создаем суперпользователя..."
python3.10 manage.py createsuperuser --noinput --username admin --email admin@example.com || echo "Суперпользователь уже существует"

# 7. Настройка прав доступа
echo "🔐 Настраиваем права доступа..."
chmod 755 $PYTHONANYWHERE_PATH
chmod 644 $PYTHONANYWHERE_PATH/db.sqlite3
chmod -R 755 $PYTHONANYWHERE_PATH/staticfiles
chmod -R 755 $PYTHONANYWHERE_PATH/media

# 8. Создание файла конфигурации WSGI
echo "⚙️ Создаем конфигурацию WSGI..."
cat > $PYTHONANYWHERE_PATH/passenger_wsgi.py << 'EOF'
import os
import sys

# Добавляем путь к проекту (используем Working directory)
path = '/home/Viktor811/CookBook'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_pythonanywhere')

application = get_wsgi_application()
EOF

# 9. Создание файла requirements.txt для PythonAnywhere
echo "📋 Создаем requirements.txt для PythonAnywhere..."
cat > $PYTHONANYWHERE_PATH/requirements_pythonanywhere.txt << 'EOF'
Django==5.1.1
Pillow==10.0.1
python-decouple==3.8
EOF

# 10. Создание инструкций по настройке
echo "📖 Создаем инструкции по настройке..."
cat > $PYTHONANYWHERE_PATH/PYTHONANYWHERE_SETUP.md << 'EOF'
# Настройка проекта CookBook на PythonAnywhere

## 1. Настройка веб-приложения
1. Перейдите в раздел "Web" на PythonAnywhere
2. Создайте новое веб-приложение
3. Выберите "Manual configuration"
4. Укажите путь к проекту: `/home/Viktor811/CookBook`

## 2. Настройка статических файлов
В разделе "Static files":
- URL: `/static/`
- Directory: `/home/Viktor811/CookBook/staticfiles`

- URL: `/media/`
- Directory: `/home/Viktor811/CookBook/media`

## 3. Настройка WSGI
Замените содержимое файла WSGI на:
```python
import os
import sys

path = '/home/Viktor811/CookBook'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_pythonanywhere')

application = get_wsgi_application()
```

## 4. Перезапуск веб-приложения
Нажмите кнопку "Reload" в разделе "Web"

## 5. Проверка работы
Откройте ваш сайт: https://Viktor811.pythonanywhere.com

## Возможные проблемы и решения

### Проблема: Статические файлы не загружаются
**Решение:**
1. Проверьте настройки статических файлов
2. Выполните: `python3.10 manage.py collectstatic --noinput`
3. Очистите кэш браузера

### Проблема: AJAX запросы не работают
**Решение:**
1. Проверьте консоль браузера (F12)
2. Используйте fallback режим (кнопка "Простой выбор")
3. Проверьте настройки CSRF

### Проблема: Чекбокс маленький
**Решение:**
1. Проверьте загрузку CSS файлов
2. Используйте inline стили (уже добавлены)
3. Проверьте JavaScript в консоли

## Логи для отладки
Логи доступны в файле: `/home/Viktor811/CookBook/debug.log`
EOF

echo "✅ Деплой завершен!"
echo "📖 Инструкции по настройке сохранены в файле: PYTHONANYWHERE_SETUP.md"
echo "🌐 Не забудьте настроить веб-приложение в разделе 'Web' на PythonAnywhere"
