# recipes/urls.py
from django.urls import path
from .views import RecipeDetailView, RecipeListView, MyRecipesView, \
    IngredientListView, IngredientCreateView, recipe_create, recipe_edit, recipe_delete, \
    CategoryListView, get_ingredient_unit, get_ingredient_name, api_search_recipes, api_search_ingredients, api_create_ingredient, ingredient_management

urlpatterns = [
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("add/", recipe_create, name="recipe_add"),
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("my-recipes/", MyRecipesView.as_view(), name="my_recipes"),
    path("<int:pk>/edit/", recipe_edit, name="recipe_edit"),
    path("<int:pk>/delete/", recipe_delete, name="recipe_delete"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient_list"),
    path("ingredients/add/", IngredientCreateView.as_view(), name="ingredient_add"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("api/ingredient-unit/", get_ingredient_unit, name="get_ingredient_unit"),
    path("api/ingredient-name/<int:ingredient_id>/", get_ingredient_name, name="get_ingredient_name"),
    path("api/search/", api_search_recipes, name="api_search_recipes"),
    path("api/search-ingredients/", api_search_ingredients, name="api_search_ingredients"),
    path("api/create-ingredient/", api_create_ingredient, name="api_create_ingredient"),
    path("ingredients/manage/", ingredient_management, name="ingredient_management"),
]
