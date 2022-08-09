from django.db import models


class Category(models.Model):
    CATEGORY_CHOICES = (
        ('books', 'Книги'),
        ('films', 'Фильмы'),
        ('music', 'Музыка'),
    )
    name = models.CharField(max_length=256, choices=CATEGORY_CHOICES)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    GENRE_CHOICES = (
        ('drama', 'Драма'),
        ('comedy', 'Комедия'),
        ('western', 'Вестерн'),
        ('fantasy', 'Фэнтези'),
        ('sci-fi', 'Фантастика'),
        ('detective', 'Детектив'),
        ('thriller', 'Триллер'),
        ('tale', 'Сказка'),
        ('gonzo', 'Гонзо'),
        ('roman', 'Роман'),
        ('ballad', 'Баллада'),
        ('rock-n-roll', 'Rock-n-roll'),
        ('classical', 'Классика'),
        ('rock', 'Рок'),
        ('chanson', 'Шансон'),
    )
    name = models.CharField(max_length=256, choices=GENRE_CHOICES)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name

