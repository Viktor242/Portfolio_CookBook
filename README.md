# 🍲 CookBook

Учебный проект на Django для командной разработки. Веб-приложение для создания, хранения и поиска кулинарных рецептов.

## 📦 Структура проекта
- **users** — регистрация, авторизация, профиль пользователя  
- **recipes** — добавление, редактирование и просмотр рецептов  
- **collections_app** — подборки рецептов пользователей  
- **search** — поиск и фильтры по рецептам  
- **templates/main** — общие HTML-шаблоны (base, home, login, profile, register)  

## 🚀 Запуск проекта

### Локальная разработка

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/Viktor242/CookBook.git
   cd CookBook
   ```

2. Создать виртуальное окружение и установить зависимости:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate    # для Windows
   # или
   source .venv/bin/activate # для Linux/Mac
   pip install -r requirements.txt
   ```

3. Применить миграции и запустить сервер:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # создать админа
   python manage.py runserver
   ```

4. Открыть в браузере:
   - http://127.0.0.1:8000/ — главная  
   - http://127.0.0.1:8000/users/ — пользователи  
   - http://127.0.0.1:8000/recipes/ — рецепты  
   - http://127.0.0.1:8000/collections/ — коллекции  
   - http://127.0.0.1:8000/search/ — поиск
   - http://127.0.0.1:8000/admin/ — админка

### Деплой на PythonAnywhere

Подробная инструкция по деплою доступна в файле [DEPLOYMENT.md](DEPLOYMENT.md)

**Быстрый деплой:**
1. Клонируйте репозиторий на PythonAnywhere
2. Установите зависимости: `python3.10 -m pip install --user -r requirements.txt`
3. Примените миграции: `python3.10 manage.py migrate`
4. Соберите статические файлы: `python3.10 manage.py collectstatic --noinput`
5. Настройте Web App в панели PythonAnywhere
6. Перезапустите приложение

**Живая версия:** https://viktor811.pythonanywhere.com/

## 🛠 Технологии

- **Backend:** Django 4.2, Python 3.10+
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **База данных:** SQLite (разработка), PostgreSQL (продакшн)
- **Деплой:** PythonAnywhere
- **Версионный контроль:** Git, GitHub

## 📁 Структура файлов

```
CookBook/
├── config/                 # Настройки Django
│   ├── settings.py        # Основные настройки
│   ├── urls.py           # Главный URL-роутер
│   └── wsgi.py           # WSGI конфигурация
├── users/                 # Приложение пользователей
├── recipes/               # Приложение рецептов
├── collections_app/       # Приложение коллекций
├── search/                # Приложение поиска
├── templates/             # HTML шаблоны
├── static/                # Статические файлы (CSS, JS, изображения)
├── media/                 # Медиа файлы (загруженные пользователями)
├── staticfiles/           # Собранные статические файлы для продакшна
├── manage.py              # Django management script
├── requirements.txt       # Python зависимости
└── README.md              # Документация проекта
```

## 🔧 Основные функции

- **Регистрация и авторизация** пользователей
- **Создание и редактирование** рецептов с фотографиями
- **Система ингредиентов** с единицами измерения
- **Категории рецептов** для удобной навигации
- **Коллекции рецептов** для организации
- **Поиск и фильтрация** по различным критериям
- **Комментарии и оценки** рецептов
- **Личный кабинет** пользователя

## 👥 Команда проекта

- **Виктор** — координатор, деплой  
- **Сергей** — backend (модели + админка). Сделал:  
  - кастомная модель пользователя (`users.User` с аватаром и bio),  
  - настройка `AUTH_USER_MODEL` и MEDIA,  
  - регистрация пользователя в админке,  
  - модели для `recipes` (Recipe, Ingredient, Category, RecipeIngredient, Comment, Rating) + админка,  
  - модели для `collections_app` (Collection, CollectionItem) + админка,  
  - заготовка модели `search` (SearchIndex) + админка,  
  - миграции для всех приложений.  
- **Николай** — backend (логика views)  
- **Евгений** — поиск и фильтры (JS/HTMX)  
- **Ирина** — frontend (шаблоны, верстка)

## 📝 Лицензия

Этот проект создан в учебных целях.  
