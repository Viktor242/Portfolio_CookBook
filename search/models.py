from django.db import models
from recipes.models import Recipe


# Временно отключено для исправления ошибки удаления рецептов
# class SearchIndex(models.Model):
#     recipe = models.OneToOneField(
#         Recipe, on_delete=models.CASCADE, related_name="search_index", verbose_name="Рецепт"
#     )
#     title = models.CharField("Заголовок", max_length=255)
#     content = models.TextField("Текст для поиска")
#     updated_at = models.DateTimeField("Обновлено", auto_now=True)

#     class Meta:
#         verbose_name = "Поисковый индекс"
#         verbose_name_plural = "Поисковые индексы"

#     def __str__(self):
#         return f"Индекс: {self.recipe}"
