from django.contrib.auth.models import AbstractUser
from django.db import models


def user_avatar_upload_to(instance, filename):
    return f"avatars/{instance.id or 'new'}/{filename}"


class User(AbstractUser):
    avatar = models.ImageField("Аватар", upload_to=user_avatar_upload_to, blank=True, null=True)
    bio = models.TextField("О себе", blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.get_full_name() or self.username
