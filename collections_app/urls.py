from django.urls import path
from . import views
from .views import collection_list, collection_create, collection_detail, toggle_recipe_in_collection, collection_edit, \
    collection_delete, api_user_collections, api_add_recipe_to_collection, api_remove_recipe_from_collection

urlpatterns = [
    # коллекции
    path("", collection_list, name="collection_list"),
    path("add/", collection_create, name="collection_add"),
    path("<int:pk>/", collection_detail, name="collection_detail"),
    path("<int:collection_id>/toggle/<int:recipe_id>/", toggle_recipe_in_collection, name="toggle_recipe_in_collection"),
    path("<int:pk>/edit/", collection_edit, name="collection_edit"),
    path("<int:pk>/delete/", collection_delete, name="collection_delete"),
    
    # API endpoints
    path("api/user-collections/", api_user_collections, name="api_user_collections"),
    path("api/add-recipe/", api_add_recipe_to_collection, name="api_add_recipe_to_collection"),
    path("api/remove-recipe/", api_remove_recipe_from_collection, name="api_remove_recipe_from_collection"),
]
