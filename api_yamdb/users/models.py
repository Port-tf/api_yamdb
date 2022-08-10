from django.db import models
from django.contrib.auth.models import AbstractUser


CHOICES_ROLE = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
]


class User(AbstractUser):
    email = models.EmailField('e-mail', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль пользователя', default='user', max_length=50, choices=CHOICES_ROLE)
