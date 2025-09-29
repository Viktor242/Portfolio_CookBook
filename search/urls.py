# search/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_recipes, name='search'),           # ← Поиск
    path('recipe/<int:pk>/', views.recipe_detail, name='search_detail'),  # ← Детали рецепта
]