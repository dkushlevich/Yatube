from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    image = models.ImageField(
        verbose_name='Фото профиля',
        help_text='Загрузите фото профиля',
        upload_to="users_images",
        blank=True
    )
