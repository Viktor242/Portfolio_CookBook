from decimal import Decimal, ROUND_HALF_UP
import decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import PROTECT, Avg
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField("Слаг", max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    name = models.CharField("Название", max_length=150, unique=True)
    default_unit = models.CharField("Ед. изм. (по умолч.)", max_length=32, blank=True)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    instruction = models.TextField("Инструкция")
    cook_time = models.PositiveIntegerField("Время приготовления (мин)")

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recipes",
        verbose_name="Категория",
    )

    DIFFICULTY_CHOICES = [
        ("easy", "Легко"),
        ("medium", "Средне"),
        ("hard", "Сложно"),
    ]
    difficulty = models.CharField(
        "Сложность",
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default="easy",
    )


    # Рейтинг считается автоматически по оценкам
    rating = models.DecimalField(
        "Рейтинг", max_digits=4, decimal_places=2, default=0, editable=False
    )

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    ingredients = models.ManyToManyField(
        "Ingredient",
        through="RecipeIngredient",
        related_name="recipes",
        verbose_name="Ингредиенты",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def image_tag(self):
        """Миниатюра для админки."""
        # Поле image удалено из модели Recipe
        return "—"
    image_tag.short_description = "Фото"

    def update_rating(self):
        """Пересчитать средний рейтинг из связанных оценок."""
        agg = self.ratings.aggregate(avg=Avg("value"))
        avg_value = agg["avg"]
        if avg_value is None:
            new_value = Decimal("0.00")
        else:
            try:
                # Безопасное преобразование в Decimal
                avg_str = str(avg_value)
                if avg_str.lower() in ['nan', 'inf', '-inf']:
                    new_value = Decimal("0.00")
                else:
                    new_value = Decimal(avg_str).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            except (ValueError, TypeError, decimal.InvalidOperation):
                new_value = Decimal("0.00")
        
        if self.rating != new_value:
            self.rating = new_value
            self.save(update_fields=["rating"])

    @property
    def main_image(self):
        """Вернуть главное изображение (если есть)."""
        main = self.images.filter(is_main=True).first()
        if main:
            return main.image.url
        return None


class RecipeImage(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="images", verbose_name="Рецепт"
    )
    image = models.ImageField("Изображение", upload_to="recipe_images/")
    is_main = models.BooleanField("Основное", default=False)
    position = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Изображение рецепта"
        verbose_name_plural = "Изображения рецептов"
        ordering = ["position", "id"]

    def __str__(self):
        try:
            return f"{self.recipe.title} → {self.image.name}"
        except:
            return f"Изображение → {self.image.name}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=PROTECT, related_name="ingredient_recipes"
    )
    amount = models.DecimalField("Количество", max_digits=8, decimal_places=2)
    unit = models.CharField("Ед. изм.", max_length=32, blank=True)

    class Meta:
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецепта"
        unique_together = ("recipe", "ingredient")

    def __str__(self):
        return f"{self.ingredient} — {self.amount} {self.unit}".strip()


class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments", verbose_name="Рецепт"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пользователь",
    )
    text = models.TextField("Комментарий")
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        try:
            return f"Комментарий от {self.user} к «{self.recipe}»"
        except:
            return f"Комментарий от {self.user}"


class Rating(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ratings", verbose_name="Рецепт"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="Пользователь",
    )
    value = models.PositiveSmallIntegerField("Оценка", validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ["-created_at"]
        unique_together = ("recipe", "user")

    def __str__(self):
        return f"{self.user} → {self.recipe}: {self.value}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recipe.update_rating()

    def delete(self, *args, **kwargs):
        recipe = self.recipe
        super().delete(*args, **kwargs)
        # Проверяем, что рецепт еще существует перед обновлением рейтинга
        if Recipe.objects.filter(pk=recipe.pk).exists():
            recipe.update_rating()