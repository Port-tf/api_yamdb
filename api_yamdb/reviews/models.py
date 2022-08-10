from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    genre = models.ManyToManyField(Genre, related_name='genres')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name

