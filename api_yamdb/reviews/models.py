from django.db import models

from django.contrib.auth.models import AbstractUser


CHOICES_ROLE = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
]

class User(AbstractUser):
    username = models.CharField('Ник пользователя', unique=True, max_length=150)
    email = models.EmailField('e-mail пользователя')
    first_name = models.CharField('Имя пользователя', max_length=150)
    last_name = models.CharField('Фамилия пользователя', max_length=150)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль пользователя', default='user', max_length=50, choices=CHOICES_ROLE)
