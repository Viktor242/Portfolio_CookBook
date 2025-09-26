# 🍳 Кулинарная книга - Django проект

## 📁 Структура проекта

```
CookBook/
├── config/                  # Настройки Django
│   ├── __init__.py
│   ├── settings.py         # Основные настройки проекта
│   ├── urls.py            # Главный URL-роутер
│   └── wsgi.py            # WSGI конфигурация
├── users/                   # Приложение пользователей
│   ├── __init__.py
│   ├── admin.py           # Админка пользователей
│   ├── apps.py            # Конфигурация приложения
│   ├── forms.py           # Формы регистрации/авторизации
│   ├── models.py          # Модель пользователя
│   ├── urls.py            # URL-маршруты пользователей
│   ├── views.py           # Представления пользователей
│   └── migrations/        # Миграции базы данных
├── recipes/                 # Приложение рецептов
│   ├── __init__.py
│   ├── admin.py           # Админка рецептов
│   ├── apps.py            # Конфигурация приложения
│   ├── forms.py           # Формы рецептов
│   ├── models.py          # Модели рецептов, ингредиентов, категорий
│   ├── urls.py            # URL-маршруты рецептов
│   ├── views.py           # Представления рецептов
│   └── migrations/        # Миграции базы данных
├── collections_app/         # Приложение коллекций
│   ├── __init__.py
│   ├── admin.py           # Админка коллекций
│   ├── apps.py            # Конфигурация приложения
│   ├── forms.py           # Формы коллекций
│   ├── models.py          # Модели коллекций
│   ├── urls.py            # URL-маршруты коллекций
│   ├── views.py           # Представления коллекций
│   └── migrations/        # Миграции базы данных
├── search/                  # Приложение поиска
│   ├── __init__.py
│   ├── admin.py           # Админка поиска
│   ├── apps.py            # Конфигурация приложения
│   ├── models.py          # Модели поиска
│   ├── urls.py            # URL-маршруты поиска
│   ├── views.py           # Представления поиска
│   └── migrations/        # Миграции базы данных
├── templates/               # HTML шаблоны
│   ├── main/              # Общие шаблоны
│   │   ├── base.html      # Базовый шаблон
│   │   ├── home.html      # Главная страница
│   │   ├── login.html     # Страница входа
│   │   ├── register.html  # Страница регистрации
│   │   └── profile.html   # Профиль пользователя
│   ├── recipes/           # Шаблоны рецептов
│   │   ├── recipe_list.html
│   │   ├── recipe_detail.html
│   │   ├── recipe_form.html
│   │   └── category_list.html
│   ├── users/             # Шаблоны пользователей
│   │   ├── profile.html
│   │   └── profile_edit.html
│   ├── collections/       # Шаблоны коллекций
│   │   ├── collection_list.html
│   │   ├── collection_detail.html
│   │   └── collection_form.html
│   └── search/            # Шаблоны поиска
│       ├── search.html
│       └── search_results.html
├── static/                 # Статические файлы
│   ├── css/
│   │   └── main.css       # Основные стили
│   ├── js/
│   │   └── main.js        # JavaScript функциональность
│   └── images/            # Статические изображения
├── media/                  # Медиа файлы (загружаемые пользователями)
│   ├── recipes/           # Фотографии рецептов
│   ├── recipe_images/     # Дополнительные изображения рецептов
│   └── avatars/           # Аватары пользователей
├── staticfiles/            # Собранные статические файлы (для продакшна)
├── .venv/                  # Виртуальное окружение (локально)
├── .git/                   # Git репозиторий
├── manage.py              # Django management script
├── requirements.txt       # Python зависимости
├── db.sqlite3            # База данных SQLite
├── README.md             # Документация проекта
├── DEPLOYMENT.md         # Инструкции по деплою
├── STRUCTURE.md          # Структура проекта (этот файл)
└── DATABASE_CONNECTIONS.md # Настройки базы данных
```

## 🎨 Статические файлы

### CSS (`static/css/main.css`)
- **Адаптивные стили** с Bootstrap-подобными классами
- **Современный дизайн** с градиентами и тенями
- **Анимации и переходы** для улучшения UX
- **Типографика** с системными шрифтами
- **Компоненты** для форм, кнопок, карточек

### JavaScript (`static/js/main.js`)
- **Динамическое добавление/удаление** ингредиентов и изображений
- **AJAX запросы** для получения единиц измерения
- **Валидация форм** в реальном времени
- **Поиск** с поддержкой Enter и фильтрами
- **Подтверждение удаления** через модальные окна

### Изображения (`static/images/`)
- `logo.svg` - Логотип проекта
- Иконки для интерфейса

## 📸 Медиа файлы

### Фотографии рецептов (`media/recipes/`)
- **Основные изображения** рецептов
- **Дополнительные фото** (`media/recipe_images/`)
- **Аватары пользователей** (`media/avatars/`)
- Поддерживаются форматы: JPG, PNG, GIF, WebP
- Автоматическое изменение размера

## ⚙️ Настройки Django

### Статические файлы (`config/settings.py`)
```python
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Папка со статическими файлами проекта
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # Для collectstatic
```

### Медиа файлы
```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### База данных
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Пользователи
```python
AUTH_USER_MODEL = 'users.User'
```

## 🚀 Запуск проекта

### Локальная разработка
1. **Клонирование репозитория:**
   ```bash
   git clone https://github.com/Viktor242/CookBook.git
   cd CookBook
   ```

2. **Создание виртуального окружения:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   source .venv/bin/activate # Linux/Mac
   ```

3. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Миграции базы данных:**
   ```bash
   python manage.py migrate
   ```

5. **Создание суперпользователя:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Запуск сервера разработки:**
   ```bash
   python manage.py runserver
   ```

### Продакшн (PythonAnywhere)
1. **Сбор статических файлов:**
   ```bash
   python3.10 manage.py collectstatic --noinput
   ```

2. **Настройка Web App** в панели PythonAnywhere
3. **Перезапуск приложения**

## 📱 Особенности

- **Современный дизайн** - адаптивный интерфейс
- **Интерактивные формы** - динамическое добавление элементов
- **AJAX функциональность** - обновление без перезагрузки
- **Мобильная адаптация** - работает на всех устройствах
- **Быстрая загрузка** - оптимизированные ресурсы

## 🎯 Функциональность

### Пользователи
- ✅ Регистрация и авторизация
- ✅ Профиль с аватаром и биографией
- ✅ Личный кабинет

### Рецепты
- ✅ Создание и редактирование рецептов
- ✅ Загрузка фотографий (основная + дополнительные)
- ✅ Система ингредиентов с единицами измерения
- ✅ Категории рецептов
- ✅ Поиск и фильтрация
- ✅ Рейтинги и комментарии

### Коллекции
- ✅ Создание коллекций рецептов
- ✅ Добавление рецептов в коллекции
- ✅ Управление коллекциями

### Поиск
- ✅ Поиск по названию и описанию
- ✅ Фильтрация по категориям
- ✅ Фильтр по наличию изображений
- ✅ Сортировка результатов

## 🔧 Технологии

- **Backend:** Django 4.2, Python 3.10+
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **База данных:** SQLite3 (разработка), PostgreSQL (продакшн)
- **Стили:** CSS Grid, Flexbox, CSS переменные
- **JavaScript:** Fetch API, DOM manipulation
- **Деплой:** PythonAnywhere

## 🎨 Дизайн

- **Цветовая схема:** Синий (#007bff), серый (#6c757d), белый
- **Шрифты:** Системные шрифты (Inter, -apple-system, BlinkMacSystemFont)
- **Стиль:** Современный, минималистичный
- **Компоненты:** Карточки, кнопки, формы, модальные окна
- **Анимации:** Плавные переходы и hover-эффекты

## 📊 Модели данных

### User (пользователь)
- username, email, password
- avatar, bio
- date_joined, last_login

### Recipe (рецепт)
- title, description, instructions
- author, category
- image, cooking_time, servings
- created_at, updated_at

### Ingredient (ингредиент)
- name, default_unit
- created_at

### Category (категория)
- name, description
- created_at

### Collection (коллекция)
- name, description
- author, recipes
- created_at, updated_at
