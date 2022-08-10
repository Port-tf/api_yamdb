from rest_framework import serializers
from reviews.models import Category, Genre, Titles
import datetime as dt


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = ('name', 'year', 'genre', 'category', 'description')

    def validate_year(self, value):
        """Проверяет год выхода произведения"""
        current_year = dt.date.today().year
        if (value > current_year):
            raise serializers.ValidationError(
                'Год произведения не может быть больше текущего'
            )
        return value

    def validate_genre(self, value):
        """Проверяет, что жанр есть в списке доступных"""
        genre = Genre.objects.all()
        if value not in genre:
            raise serializers.ValidationError('Выберите жанр из списка')
        return value

    def validate_category(self, value):
        """Проверяет, что категория есть в списке доступных"""
        category = Category.objects.all()
        if value not in category:
            raise serializers.ValidationError('Выберите категорию из списка')
        return value
