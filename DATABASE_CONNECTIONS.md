# Связи формы рецепта с базой данных

## ✅ Все поля формы связаны с моделями Django

### 1. Основные поля рецепта (Recipe модель)
- **Название рецепта** → `Recipe.title` (CharField)
- **Описание** → `Recipe.description` (TextField)
- **Инструкция приготовления** → `Recipe.instruction` (TextField)
- **Время приготовления** → `Recipe.cook_time` (PositiveIntegerField)
- **Категория** → `Recipe.category` (ForeignKey → Category)
- **Сложность** → `Recipe.difficulty` (CharField с choices)

### 2. Ингредиенты (RecipeIngredient модель через formset)
- **Ингредиент** → `RecipeIngredient.ingredient` (ForeignKey → Ingredient)
- **Количество** → `RecipeIngredient.amount` (DecimalField)
- **Единица измерения** → `RecipeIngredient.unit` (CharField с choices)

### 3. Изображения (RecipeImage модель через formset)
- **Изображение** → `RecipeImage.image` (ImageField)
- **Основное изображение** → `RecipeImage.is_main` (BooleanField)

## 🔗 Связанные модели

### Ingredient модель
- `name` - название ингредиента
- `default_unit` - единица измерения по умолчанию
- **API endpoint**: `/recipes/api/ingredient-unit/` для получения default_unit

### Category модель
- `name` - название категории
- `slug` - слаг для URL

## 🎯 Автоматические функции

1. **Автовыбор единиц измерения**: При выборе ингредиента автоматически выбирается его default_unit
2. **AJAX запросы**: Получение единиц измерения из базы данных в реальном времени
3. **Валидация**: Все обязательные поля проверяются на стороне сервера
4. **Связанные данные**: Категории и ингредиенты загружаются из базы данных

## 📊 Текущие данные в базе

### Ингредиенты:
- Молоко (default_unit: мл)
- Соль (default_unit: г)  
- Яйца (default_unit: шт)

### Категории:
- Завтраки
- Обеды
- Ужины

## ✅ Статус: ВСЕ ПОЛЯ СВЯЗАНЫ С БАЗОЙ ДАННЫХ
