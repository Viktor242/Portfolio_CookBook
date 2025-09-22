# recipes/urls.py
from django.urls import path
from .views import RecipeDetailView, RecipeListView, MyRecipesView, \
    IngredientListView, IngredientCreateView, recipe_create, recipe_edit

urlpatterns = [
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("add/", recipe_create, name="recipe_add"),
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("my-recipes/", MyRecipesView.as_view(), name="my_recipes"),
    path("<int:pk>/edit/", recipe_edit, name="recipe_edit"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient_list"),
    path("ingredients/add/", IngredientCreateView.as_view(), name="ingredient_add"),
]
