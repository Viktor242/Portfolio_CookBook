from django.urls import path
from . import views
from .views import collection_list, collection_create, collection_detail, toggle_recipe_in_collection, collection_edit, \
    collection_delete

urlpatterns = [
    # коллекции
    path("", collection_list, name="collection_list"),
    path("add/", collection_create, name="collection_add"),
    path("<int:pk>/", collection_detail, name="collection_detail"),
    path("<int:collection_id>/toggle/<int:recipe_id>/", toggle_recipe_in_collection, name="toggle_recipe_in_collection"),
    path("<int:pk>/edit/", collection_edit, name="collection_edit"),
    path("<int:pk>/delete/", collection_delete, name="collection_delete"),
]
