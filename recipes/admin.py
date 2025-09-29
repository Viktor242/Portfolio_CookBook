from django.contrib import admin, messages
from django.db.models import ProtectedError
from django.utils.html import format_html

from .models import Category, Ingredient, Recipe, RecipeIngredient, Comment, Rating, RecipeImage


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
                level=messages.ERROR,
            )

class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # на случай, если метод на модели ещё не подхватился — дублируем рендер миниатюры
    def image_tag(self, obj):
        if obj.images.exists():
            first_image = obj.images.first()
            return format_html('<img src="{}" style="max-height:60px;"/>', first_image.image.url)
        return "—"
    image_tag.short_description = "Фото"

    list_display = (
        "title",
        "author",
        "category",
        "difficulty",
        "cook_time",
        "rating",
        "image_tag",
        "created_at",
    )
    list_filter = ("category", "difficulty")
    search_fields = ("title", "description")
    autocomplete_fields = ["author", "category"]
    readonly_fields = ("rating", "image_tag")
    inlines = [RecipeIngredientInline, CommentInline, RatingInline, RecipeImageInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user", "text", "created_at")
    search_fields = ("text",)
    autocomplete_fields = ["recipe", "user"]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user", "value", "created_at")
    list_filter = ("value",)
    autocomplete_fields = ["recipe", "user"]



