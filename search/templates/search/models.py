from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title