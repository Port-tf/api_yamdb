from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import LIMIT_TEXT
from users.models import User


class Category(models.Model):
    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField('Страница категории', unique=True, max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField('Страница жанра', unique=True, max_length=100)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанры', related_name='titles')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='titles'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=10)
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[LIMIT_TEXT]


class Comments(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )

    def __str__(self):
        return self.text[LIMIT_TEXT]
