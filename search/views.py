from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from recipes.models import Recipe, Category

def search_recipes(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    min_cook_time = request.GET.get('min_cook_time', '').strip()
    max_cook_time = request.GET.get('max_cook_time', '').strip()
    has_image = request.GET.get('has_image', '')
    sort_by = request.GET.get('sort', '')

    # Базовый запрос рецептов
    recipes = Recipe.objects.select_related('author', 'category').prefetch_related('ingredients', 'images')
    
    # Для гостей показываем только публичные рецепты (если есть такое поле)
    # Если поля is_public нет, показываем все рецепты
    if not request.user.is_authenticated:
        # Предполагаем, что есть поле is_public или is_published
        # Если такого поля нет, можно убрать эту строку
        recipes = recipes.filter(is_public=True) if hasattr(Recipe, 'is_public') else recipes

    # Поиск по тексту
    if query:
        words = query.split()
        q_objects = Q()

        for word in words:
            q_objects |= (
                    Q(title__iregex=word) |  # iregex вместо icontains
                    Q(description__iregex=word) |
                    Q(instruction__iregex=word) |
                    Q(category__name__iregex=word) |
                    Q(author__username__iregex=word) |
                    Q(ingredients__name__iregex=word)
            )

        recipes = recipes.filter(q_objects).distinct()

    # Фильтр по категории
    if category_slug:
        recipes = recipes.filter(category__slug=category_slug)

    # Фильтр по сложности
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)

    # Фильтр по времени приготовления — ОТ
    if min_cook_time:
        try:
            min_val = int(min_cook_time)
            recipes = recipes.filter(cook_time__gte=min_val)
        except ValueError:
            pass  # Некорректный ввод — игнорируем

    # Фильтр по времени приготовления — ДО
    if max_cook_time:
        try:
            max_val = int(max_cook_time)
            recipes = recipes.filter(cook_time__lte=max_val)
        except ValueError:
            pass  # Некорректный ввод — игнорируем

    # Фильтр по наличию картинки
    if has_image == 'yes':
        # Рецепты с основным изображением ИЛИ с дополнительными изображениями
        recipes = recipes.filter(
            Q(image__isnull=False) & ~Q(image='') | Q(images__isnull=False)
        ).distinct()
    elif has_image == 'no':
        # Рецепты без основного изображения И без дополнительных изображений
        recipes = recipes.filter(
            (Q(image__isnull=True) | Q(image='')) & ~Q(images__isnull=False)
        ).distinct()

    # 🔥 СОРТИРОВКА — ключевой шаг!
    sort_options = {
        'newest': '-created_at',           # от новых к старым
        'oldest': 'created_at',            # от старых к новым
        'rating_high': '-rating',          # от высокого к низкому
        'rating_low': 'rating',            # от низкого к высокому
        'time_short': 'cook_time',         # от быстрых к долгим
        'time_long': '-cook_time',         # от долгих к быстрым
        'title_a_z': 'title',              # от А до Я
        'title_z_a': '-title',             # от Я до А
    }

    # Применяем сортировку, если выбрана
    if sort_by in sort_options:
        recipes = recipes.order_by(sort_options[sort_by])
    else:
        # По умолчанию — сортировка по новизне
        recipes = recipes.order_by('-created_at')

    # ПАГИНАЦИЯ
    paginator = Paginator(recipes, 10)  # 10 рецептов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем все категории для выпадающего списка
    categories = Category.objects.all()

    return render(request, 'search/results.html', {
        'recipes': page_obj,  # ← ВАЖНО: передаём page_obj, а не recipes
        'query': query,
        'categories': categories,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'min_cook_time': min_cook_time,
        'max_cook_time': max_cook_time,
        'sort_by': sort_by,
        'has_image': has_image,
        'page_obj': page_obj,  # ← Передаём для пагинации
        'is_guest': not request.user.is_authenticated,  # Флаг для гостей
    })

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'search/detail.html', {'recipe': recipe})