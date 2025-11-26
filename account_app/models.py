from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save_avatar(instance, filename):
        return f"users/{instance.pk}/avatar/{filename}"

    avatar = models.ImageField(upload_to='avatars', default='default/avatar.png', null=True, blank=True)

    def __str__(self):
        return self.username
