from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from recipes.forms import RecipeForm, CommentForm, RatingForm, RecipeIngredientFormSet, RecipeIngredientFormSetCreate, RecipeImageFormSet, RecipeImageFormSetCreate
from recipes.models import Recipe, Rating, Ingredient, Category

PREFIX = "ingredients"

def index(request):
    return HttpResponse("Раздел рецептов работает!")

class HomePageView(ListView):
    """Главная страница — приветствие и несколько рецептов"""
    model = Recipe
    template_name = "main/home.html"
    context_object_name = "recipes"

    def get_queryset(self):
        return Recipe.objects.order_by("-created_at")[:5]  # последние 5 рецептов
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['query'] = self.request.GET.get('q', '')
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


@login_required
def recipe_create(request):
    prefix_ingredients = "ingredients"
    prefix_images = "images"

    if request.method == "POST":
        form = RecipeForm(request.POST)
        formset_ingredients = RecipeIngredientFormSetCreate(
            request.POST, prefix=prefix_ingredients
        )
        image_formset = RecipeImageFormSetCreate(
            request.POST, request.FILES, prefix=prefix_images
        )

        # Проверяем валидность всех форм
        form_valid = form.is_valid()
        ingredients_valid = formset_ingredients.is_valid()
        images_valid = image_formset.is_valid()
        
        print(f"CREATE - Form valid: {form_valid}")
        print(f"CREATE - Ingredients formset valid: {ingredients_valid}")
        print(f"CREATE - Images formset valid: {images_valid}")
        
        if form_valid and ingredients_valid and images_valid:
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            formset_ingredients.instance = recipe
            image_formset.instance = recipe
            formset_ingredients.save()
            image_formset.save()
            print(f"CREATE - Рецепт {recipe.title} успешно создан!")
            return redirect("recipe_detail", pk=recipe.pk)
        else:
            # Если есть ошибки, показываем их
            print("CREATE - Ошибки валидации:")
            if not form_valid:
                print(f"CREATE - Form errors: {form.errors}")
            if not ingredients_valid:
                print(f"CREATE - Formset ingredients errors: {formset_ingredients.errors}")
                print(f"CREATE - Formset ingredients non_form_errors: {formset_ingredients.non_form_errors()}")
            if not images_valid:
                print(f"CREATE - Image formset errors: {image_formset.errors}")
                print(f"CREATE - Image formset non_form_errors: {image_formset.non_form_errors()}")
    else:
        form = RecipeForm()
        recipe = Recipe()
        formset_ingredients = RecipeIngredientFormSetCreate(
            instance=recipe, prefix=prefix_ingredients
        )
        image_formset = RecipeImageFormSetCreate(
            instance=recipe, prefix=prefix_images
        )

    return render(
        request,
        "recipes/recipe_form.html",
        {
            "form": form,
            "formset": formset_ingredients,
            "image_formset": image_formset,
            "ingredients": Ingredient.objects.all().order_by('name'),  # Добавляем ингредиенты для fallback
            "editing": False,
        },
    )


@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return HttpResponseForbidden("Нет доступа")

    prefix_ingredients = "ingredients"
    prefix_images = "images"

    if request.method == "POST":
        print(f"DEBUG: POST данные: {dict(request.POST)}")
        print(f"DEBUG: FILES данные: {dict(request.FILES)}")
        
        form = RecipeForm(request.POST, instance=recipe)
        formset_ingredients = RecipeIngredientFormSet(
            request.POST, instance=recipe, prefix=prefix_ingredients
        )
        image_formset = RecipeImageFormSet(
            request.POST, request.FILES, instance=recipe, prefix=prefix_images
        )

        # Проверяем валидность каждой формы отдельно
        form_valid = form.is_valid()
        ingredients_valid = formset_ingredients.is_valid()
        images_valid = image_formset.is_valid()
        
        print(f"Form valid: {form_valid}")
        print(f"Ingredients formset valid: {ingredients_valid}")
        print(f"Images formset valid: {images_valid}")
        
        # Дополнительная проверка дубликатов ингредиентов
        duplicate_ingredients = []
        if ingredients_valid:
            ingredient_ids = []
            for ingredient_form in formset_ingredients.forms:
                if (ingredient_form.cleaned_data and 
                    ingredient_form.cleaned_data.get('ingredient') and 
                    ingredient_form.cleaned_data.get('amount') and 
                    not ingredient_form.cleaned_data.get('DELETE')):
                    ingredient_id = ingredient_form.cleaned_data.get('ingredient').pk
                    if ingredient_id in ingredient_ids:
                        # Найден дубликат
                        ingredient_name = ingredient_form.cleaned_data.get('ingredient').name
                        duplicate_ingredients.append(ingredient_name)
                    else:
                        ingredient_ids.append(ingredient_id)
        
        if duplicate_ingredients:
            # Добавляем ошибку в formset
            duplicate_names = ', '.join(duplicate_ingredients)
            formset_ingredients.add_error(None, f"⚠️ Внимание: Ингредиенты '{duplicate_names}' добавлены несколько раз. Удалите дубликаты или выберите другие ингредиенты.")
            ingredients_valid = False
        
        if form_valid and ingredients_valid and images_valid:
            saved_recipe = form.save()
            formset_ingredients.instance = saved_recipe
            image_formset.instance = saved_recipe
            
            # Дополнительная проверка перед сохранением ингредиентов
            for ingredient_form in formset_ingredients.forms:
                if ingredient_form.cleaned_data:
                    # Если форма пустая (нет ингредиента или количества), помечаем для удаления
                    if not ingredient_form.cleaned_data.get('ingredient') or not ingredient_form.cleaned_data.get('amount'):
                        ingredient_form.cleaned_data['DELETE'] = True
                else:
                    # Если cleaned_data пустой, создаем пустой словарь с DELETE=True
                    ingredient_form.cleaned_data = {'DELETE': True}
            
            # Сохраняем formset
            formset_ingredients.save()
            image_formset.save()
            print(f"Рецепт {saved_recipe.title} успешно сохранен!")
            return redirect("my_recipes")
        else:
            # Если есть ошибки, показываем их
            print("Ошибки валидации:")
            if not form_valid:
                print(f"Form errors: {form.errors}")
            if not ingredients_valid:
                print(f"Formset ingredients errors: {formset_ingredients.errors}")
                print(f"Formset ingredients non_form_errors: {formset_ingredients.non_form_errors()}")
            if not images_valid:
                print(f"Image formset errors: {image_formset.errors}")
                print(f"Image formset non_form_errors: {image_formset.non_form_errors()}")
    else:
        form = RecipeForm(instance=recipe)
        formset_ingredients = RecipeIngredientFormSet(instance=recipe, prefix=prefix_ingredients)
        image_formset = RecipeImageFormSet(instance=recipe, prefix=prefix_images)

    return render(
        request,
        "recipes/recipe_form.html",
        {
            "form": form,
            "formset": formset_ingredients,
            "image_formset": image_formset,
            "editing": True,
            "ingredients": Ingredient.objects.all().order_by('name'),  # Добавляем ингредиенты для fallback
        },
    )

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return HttpResponseForbidden("Нет доступа")

    if request.method == "POST":
        recipe.delete()
        return redirect("my_recipes")

    return render(request, "recipes/recipe_confirm_delete.html", {
        "recipe": recipe,
    })

class RecipeDetailView(DetailView):
    """Страница рецепта с комментариями и оценками"""
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["rating_form"] = RatingForm()
        context["comments"] = self.object.comments.all()
        if self.request.user.is_authenticated:
            collections = self.request.user.collections.all()
            recipe = self.get_object()
            context["collections"] = [
                {"obj": c, "in_collection": c.items.filter(recipe=recipe).exists()}
                for c in collections
            ]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "text" in request.POST:  # комментарий
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.recipe = self.object
                comment.user = request.user
                comment.save()
                return redirect("recipe_detail", pk=self.object.pk)

        if "value" in request.POST:  # оценка
            form = RatingForm(request.POST)
            if form.is_valid():
                Rating.objects.update_or_create(
                    recipe=self.object,
                    user=request.user,
                    defaults={"value": form.cleaned_data["value"]},
                )
                return redirect("recipe_detail", pk=self.object.pk)

        return self.get(request, *args, **kwargs)

class RecipeListView(ListView):
    """Список всех рецептов"""
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 10  # по 10 рецептов на страницу

    def get_queryset(self):
        return Recipe.objects.order_by("-created_at")

class MyRecipesView(LoginRequiredMixin, ListView):
    """Список рецептов текущего пользователя"""
    model = Recipe
    template_name = "recipes/my_recipes.html"
    context_object_name = "recipes"
    paginate_by = 10

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user).order_by("-created_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['query'] = self.request.GET.get('q', '')
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class IngredientListView(LoginRequiredMixin, ListView):
    """Список всех ингредиентов"""
    model = Ingredient
    template_name = "recipes/ingredient_list.html"
    context_object_name = "ingredients"
    paginate_by = 20

    def get_queryset(self):
        return Ingredient.objects.order_by("name")


class IngredientCreateView(LoginRequiredMixin, CreateView):
    """Добавление нового ингредиента"""
    model = Ingredient
    template_name = "recipes/ingredient_form.html"
    fields = ["name", "default_unit"]
    success_url = reverse_lazy("ingredient_list")


class CategoryListView(ListView):
    """Список всех категорий"""
    model = Category
    template_name = "recipes/category_list.html"
    context_object_name = "categories"
    paginate_by = 20

    def get_queryset(self):
        return Category.objects.order_by("name")


@require_http_methods(["GET"])
def get_ingredient_name(request, ingredient_id):
    """API для получения названия ингредиента по ID"""
    try:
        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
        return JsonResponse({"name": ingredient.name})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def get_ingredient_unit(request):
    """API endpoint для получения единиц измерения ингредиента"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ingredient_id = data.get('ingredient_id')

            if ingredient_id:
                ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
                return JsonResponse({
                    'success': True,
                    'default_unit': ingredient.default_unit or ''
                })
            else:
                return JsonResponse({'success': False, 'error': 'No ingredient ID provided'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Only POST method allowed'})


@csrf_exempt
def api_search_recipes(request):
    """API endpoint для поиска и фильтрации рецептов"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '').strip()
            category = data.get('category', '').strip()
            min_rating = data.get('min_rating', '')
            max_time = data.get('max_time', '')
            ingredient = data.get('ingredient', '')
            ingredient_name = data.get('ingredient_name', '').strip()
            difficulty = data.get('difficulty', '').strip()
            
            print(f"Filter API called with query: '{query}', category: '{category}', min_rating: '{min_rating}', ingredient_name: '{ingredient_name}', difficulty: '{difficulty}'")
            
            # Проверяем общее количество рецептов
            total_recipes = Recipe.objects.count()
            print(f"Total recipes in database: {total_recipes}")
            
            # Проверяем рейтинги в базе данных
            if total_recipes > 0:
                ratings = Recipe.objects.values_list('rating', flat=True)
                print(f"Ratings in database: {list(ratings)}")
                
                # Пересчитываем рейтинги для всех рецептов
                for recipe in Recipe.objects.all():
                    recipe.update_rating()
                print("Ratings recalculated")
            
            # Базовый запрос
            recipes = Recipe.objects.select_related('author', 'category').prefetch_related('ingredients', 'images')
            
            # Фильтр по тексту
            if query:
                recipes = recipes.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(ingredients__ingredient__name__icontains=query)
                ).distinct()
            
            # Фильтр по категории
            if category:
                recipes = recipes.filter(category__slug=category)
            
            # Фильтр по минимальному рейтингу
            if min_rating:
                try:
                    min_rating_float = float(min_rating)
                    print(f"Filtering by rating >= {min_rating_float}")
                    recipes = recipes.filter(rating__gte=min_rating_float)
                    print(f"After rating filter: {recipes.count()} recipes")
                except ValueError:
                    print(f"Invalid rating value: {min_rating}")
                    pass
            
            # Фильтр по ингредиенту (по названию)
            if ingredient_name:
                print(f"Filtering by ingredient name: '{ingredient_name}'")
                # Используем iregex для поиска по частичным совпадениям
                recipes = recipes.filter(ingredients__name__iregex=ingredient_name)
                print(f"After ingredient name filter: {recipes.count()} recipes")
            
            # Фильтр по ингредиенту (по ID - для обратной совместимости)
            if ingredient:
                try:
                    ingredient_id = int(ingredient)
                    print(f"Filtering by ingredient ID: {ingredient_id}")
                    recipes = recipes.filter(ingredients__id=ingredient_id)
                    print(f"After ingredient ID filter: {recipes.count()} recipes")
                except ValueError:
                    print(f"Invalid ingredient ID: {ingredient}")
            
            # Фильтр по сложности
            if difficulty:
                print(f"Filtering by difficulty: {difficulty}")
                recipes = recipes.filter(difficulty=difficulty)
                print(f"After difficulty filter: {recipes.count()} recipes")
            
            # Ограничиваем количество результатов
            recipes = recipes.order_by('-created_at')[:20]
            
            print(f"Found {recipes.count()} recipes")
            
            # Формируем ответ
            recipes_data = []
            for recipe in recipes:
                try:
                    recipes_data.append({
                        'id': recipe.id,
                        'title': recipe.title,
                        'description': recipe.description[:100] + '...' if recipe.description and len(recipe.description) > 100 else recipe.description,
                        'author': recipe.author.username,
                        'rating': float(recipe.rating),
                        'cook_time': recipe.cook_time,
                        'difficulty': recipe.difficulty,
                        'difficulty_display': recipe.get_difficulty_display(),
                        'category': recipe.category.name if recipe.category else None,
                        'image_url': None,  # Поле image удалено из модели Recipe
                        'url': f'/recipes/{recipe.id}/'
                    })
                except Exception as e:
                    print(f"Error processing recipe {recipe.id}: {e}")
                    continue
            
            return JsonResponse({
                'success': True,
                'recipes': recipes_data,
                'count': len(recipes_data),
                'total_recipes': total_recipes
            })
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        except Exception as e:
            print(f"Filter API error: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Only POST method allowed'})


@csrf_exempt
@require_http_methods(["POST"])
def api_search_ingredients(request):
    """API endpoint для поиска ингредиентов"""
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        
        print(f"DEBUG: Поиск ингредиентов, запрос: '{query}'")
        print(f"DEBUG: Длина запроса: {len(query)}")
        print(f"DEBUG: Коды символов: {[ord(c) for c in query]}")
        
        if len(query) < 2:
            # Если запрос пустой, возвращаем все ингредиенты (для загрузки существующих)
            ingredients = Ingredient.objects.all().order_by('name')
            print(f"DEBUG: Загружаем все ингредиенты, найдено: {ingredients.count()}")
        else:
            # Поиск ингредиентов по части названия (без учета регистра)
            # Используем iregex для более надежного поиска без учета регистра
            ingredients = Ingredient.objects.filter(
                name__iregex=query
            ).order_by('name')[:10]  # Ограничиваем 10 результатами
            
            # Дополнительная отладка
            print(f"DEBUG: Поиск по '{query}', найдено: {ingredients.count()}")
            print(f"DEBUG: Запрос в БД: name__iregex='{query}'")
            
            # Проверим, есть ли ингредиенты с похожими названиями
            all_ingredients = Ingredient.objects.all()
            similar_names = [ing.name for ing in all_ingredients if query.lower() in ing.name.lower()]
            print(f"DEBUG: Похожие названия (без учета регистра): {similar_names}")
        
        ingredients_data = []
        for ingredient in ingredients:
            ingredients_data.append({
                'id': ingredient.id,
                'name': ingredient.name
            })
            print(f"DEBUG: Добавлен ингредиент: {ingredient.name}")
        
        print(f"DEBUG: Возвращаем {len(ingredients_data)} ингредиентов")
        
        return JsonResponse({
            'success': True,
            'ingredients': ingredients_data
        })
        
    except json.JSONDecodeError:
        print("DEBUG: Ошибка JSON")
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат JSON'
        })
    except Exception as e:
        print(f"DEBUG: Ошибка: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@csrf_exempt
@require_http_methods(["POST"])
def api_create_ingredient(request):
    """API endpoint для создания нового ингредиента"""
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        
        if not name:
            return JsonResponse({
                'success': False,
                'error': 'Название ингредиента не может быть пустым'
            })
        
        # Проверяем, не существует ли уже точно такой ингредиент
        if Ingredient.objects.filter(name__iexact=name).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ингредиент с таким названием уже существует'
            })
        
        # Проверяем на похожие ингредиенты (разница в 1-2 символа)
        similar_ingredients = []
        for ingredient in Ingredient.objects.all():
            if abs(len(ingredient.name) - len(name)) <= 2:
                # Простая проверка на схожесть
                if name.lower() in ingredient.name.lower() or ingredient.name.lower() in name.lower():
                    similar_ingredients.append(ingredient.name)
        
        # Если найдены похожие ингредиенты, предупреждаем пользователя
        if similar_ingredients:
            return JsonResponse({
                'success': False,
                'error': f'Возможно, вы имели в виду: {", ".join(similar_ingredients[:3])}? Проверьте правильность написания.',
                'similar': similar_ingredients[:3]
            })
        
        # Создаем новый ингредиент
        ingredient = Ingredient.objects.create(name=name)
        
        return JsonResponse({
            'success': True,
            'ingredient': {
                'id': ingredient.id,
                'name': ingredient.name
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат JSON'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def ingredient_management(request):
    """Страница управления ингредиентами"""
    ingredients = Ingredient.objects.all().order_by('name')
    
    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient_id')
        action = request.POST.get('action')
        
        if action == 'delete':
            try:
                ingredient = Ingredient.objects.get(id=ingredient_id)
                ingredient_name = ingredient.name
                ingredient.delete()
                messages.success(request, f'Ингредиент "{ingredient_name}" успешно удален!')
            except Ingredient.DoesNotExist:
                messages.error(request, 'Ингредиент не найден!')
        
        return redirect('ingredient_management')
    
    return render(request, 'recipes/ingredient_management.html', {
        'ingredients': ingredients
    })