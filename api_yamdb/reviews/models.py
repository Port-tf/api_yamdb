from django.db import models


class Category(models.Model):
    CATEGORY_CHOICE = ['Книги', 'Фильмы', 'Музыка']
    name = models.CharField(choices=CATEGORY_CHOICE)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    GENRE_CHOICE = [
        'Драма',
        'Комедия',
        'Вестерн',
        'Фэнтези',
        'Фантастика',
        'Детектив',
        'Триллер',
        'Сказка',
        'Гонзо',
        'Роман',
        'Баллада',
        'Rock-n-roll',
        'Классика',
        'Рок',
        'Шансон'
    ]
    name = models.CharField(choices=GENRE_CHOICE)
    slug = models.SlugField(unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField(max_length=4)
    genre = models.ManyToManyField(Genre, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    description = models.TextField(max_length=200)

