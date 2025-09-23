from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient, Comment, Rating


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ["ingredient"]


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    autocomplete_fields = ["user"]
    fields = ("user", "text", "created_at")
    readonly_fields = ("created_at",)


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    autocomplete_fields = ["user"]
    fields = ("user", "value", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "default_unit")
    search_fields = ("name",)
    def delete_model(self, request, obj):
        try:
            super().delete_model(request, obj)
        except ProtectedError:
            self.message_user(
                request,
                f"Нельзя удалить ингредиент «{obj.name}», так как он используется в рецептах.",
                level=messages.ERROR
            )

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "difficulty",
        "cook_time",
        "rating",
        "created_at",
    )
    list_filter = ("category", "difficulty")
    search_fields = ("title", "description")
    autocomplete_fields = ["author", "category"]
    readonly_fields = ("rating",)  # рейтинг только для просмотра
    inlines = [RecipeIngredientInline, CommentInline, RatingInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Добавили показ текста комментария в списке
    list_display = ("recipe", "user", "text", "created_at")
    search_fields = ("text",)
    autocomplete_fields = ["recipe", "user"]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user", "value", "created_at")
    list_filter = ("value",)
<<<<<<< HEAD
    autocomplete_fields = ["recipe", "user"]
=======
    autocomplete_fields = ["recipe", "user"]
>>>>>>> feature/search
