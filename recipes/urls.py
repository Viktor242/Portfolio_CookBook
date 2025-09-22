# recipes/urls.py
from django.urls import path
from .views import RecipeCreateView, RecipeDetailView, RecipeListView, MyRecipesView, RecipeUpdateView

urlpatterns = [
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("add/", RecipeCreateView.as_view(), name="recipe_add"),
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("my-recipes/", MyRecipesView.as_view(), name="my_recipes"),
    path("<int:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_edit"),
]
