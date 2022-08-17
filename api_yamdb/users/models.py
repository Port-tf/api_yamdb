from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES_ROLE = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
]


class User(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя',
        default='user',
        max_length=50,
        choices=CHOICES_ROLE)
    email = models.EmailField('E-mail пользователя', unique=True)

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'
