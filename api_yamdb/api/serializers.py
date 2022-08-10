import datetime as dt
from tkinter.tix import Tree

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comments, Genre, Review, Titles, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    
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

    # def validate_genre(self, value):
    #     """Проверяет, что жанр есть в списке доступных"""
    #     genre = Genre.objects.all()
    #     if value not in genre:
    #         raise serializers.ValidationError('Выберите жанр из списка')
    #     return value

    def validate_category(self, value):
        """Проверяет, что категория есть в списке доступных"""
        category = Category.objects.all()
        if value not in category:
            raise serializers.ValidationError('Выберите категорию из списка')
        return value


class ReviewSerializer(serializers.ModelSerializer):

    def get_score(self, obj):
        rating = self.obj.score / self.obj.score.count()
        return rating

    class Meta:
        model = Review
        fields = ('score', 'user', 'title')
        read_only_fields = ('user',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('text', 'created', 'user', 'review')
        read_only_fields = ('user',)