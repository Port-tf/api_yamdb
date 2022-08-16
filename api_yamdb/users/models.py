from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES_ROLE = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
]


class User(AbstractUser):
    # username = models.CharField(max_length=150, unique=True, null=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль пользователя', default='user',
                            max_length=50, choices=CHOICES_ROLE
                            )
    email = models.EmailField('e-mail', unique=True)

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'
