from django.db import models
from django.contrib.auth.models import AbstractUser


CHOICES_ROLE = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
]


class User(AbstractUser):

    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Рольasdgasdfafsdgasd пользователя', default='user', max_length=50, choices=CHOICES_ROLE)

    @property
    def is_user(self):
        return self.role == 'user'
    
    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'
