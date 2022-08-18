import datetime as dt
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from api_yamdb.settings import LIMIT_TEXT
from users.models import User


class AbstractModelGenreCategory(models.Model):
    """Абстрактная модель для Genre и Category"""
    name = models.CharField('Имя', max_length=256)
    slug = models.SlugField('Slug', unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']


class Category(AbstractModelGenreCategory):
    class Meta(AbstractModelGenreCategory.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = "categories"


class Genre(AbstractModelGenreCategory):
    class Meta(AbstractModelGenreCategory.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = "genres"


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        db_index=True,
        validators=[MinValueValidator(
                    limit_value=1,
                    message="Год не может быть меньше или равен нулю"),
                    MaxValueValidator(
                    limit_value=dt.date.today().year,
                    message="Год не может быть больше текущего")])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = "genres"
    

class AbstractModelReviewComments(models.Model):
    """Абстрактная модель для Review и Comments."""
    text = models.CharField(max_length=256)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews'
    )

    def __str__(self):
        return self.text[LIMIT_TEXT]

    class Meta:
        abstract = True
        ordering = ['pub_date']


class Review(AbstractModelReviewComments):
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

    class Meta(AbstractModelReviewComments.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = "reviews"
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comments(AbstractModelReviewComments):
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
    
    class Meta(AbstractModelReviewComments.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = "comments"

