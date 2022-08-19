from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from api_yamdb.settings import LIMIT_USERNAME, EMAIL_USERNAME
from .validators import UsernameRegexValidator, username_me


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOICES_ROLE = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username_validator = UsernameRegexValidator()
    username = models.CharField(
        'Логин',
        max_length=LIMIT_USERNAME,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator, username_me],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField('Имя', max_length=LIMIT_USERNAME, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя',
        default=USER,
        max_length=max(len(role[0]) for role in CHOICES_ROLE),
        choices=CHOICES_ROLE)
    email = models.EmailField('E-mail пользователя',
                              unique=True, max_length=EMAIL_USERNAME)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'), name='name_not_me')
        ]

    def __str__(self):
        return self.username
