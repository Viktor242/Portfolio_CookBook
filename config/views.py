# config/views.py
from django.shortcuts import render
from recipes.models import Recipe, Category

def home(request):
    # Получаем последние 5 рецептов
    recipes = Recipe.objects.all()[:5]
    
    # Получаем все категории для поиска
    categories = Category.objects.all()
    
    context = {
        'recipes': recipes,
        'categories': categories,
    }
    return render(request, 'main/home.html', context)
