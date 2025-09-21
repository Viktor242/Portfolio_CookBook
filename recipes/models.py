from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
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

    # Рейтинг теперь считается автоматически из таблицы Rating
    rating = models.DecimalField(
        "Рейтинг", max_digits=3, decimal_places=2, default=0, editable=False
    )

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    ingredients = models.ManyToManyField(
        Ingredient,
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

    def update_rating(self):
        """
        Пересчитывает средний рейтинг из связанных оценок.
        Округляем до сотых и пишем в DecimalField (не редактируется вручную).
        """
        agg = self.ratings.aggregate(avg=Avg("value"))
        avg_value = agg["avg"]
        if avg_value is None:
            new_value = Decimal("0.00")
        else:
            # Приводим через str, чтобы избежать артефактов float
            new_value = Decimal(str(avg_value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if self.rating != new_value:
            self.rating = new_value
            self.save(update_fields=["rating"])


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients"
    )
    # ВАЖНО: PROTECT — запретит удалить ингредиент, если он используется в рецептах
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
        return f"Комментарий от {self.user} к «{self.recipe}»"


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
    value = models.PositiveSmallIntegerField("Оценка")  # 1..5 (валидаторы можно добавить позже)
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ["-created_at"]
        unique_together = ("recipe", "user")

    def __str__(self):
        return f"{self.user} → {self.recipe}: {self.value}"

    # Автопересчёт рейтинга рецепта при добавлении/изменении/удалении оценки:
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recipe.update_rating()

    def delete(self, *args, **kwargs):
        recipe = self.recipe
        super().delete(*args, **kwargs)
        recipe.update_rating()


from django.db import models

# Create your models here.
