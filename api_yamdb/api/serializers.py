import datetime as dt
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comments, Genre, Review, Titles
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesPostSerialzier(serializers.ModelSerializer):
    """Сериайлайзер для POST, PUT, PATCH запросов"""
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
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')

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

    # def validate_category(self, value):
    #     """Проверяет, что категория есть в списке доступных"""
    #     category = Category.objects.all()
    #     if value not in category:
    #         raise serializers.ValidationError('Выберите категорию из списка')
    #     return value


class TitlesSerializer(serializers.ModelSerializer):
    """Сериайлайзер для всех запросов кроме POST, PUT, PATCH"""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'genre', 
                  'category', 'description', 'rating'
                  )

    def get_rating(self, obj):
        """Считает средний рейтинг произведения"""
        title_rating = obj.reviews.aggregate(rating=Avg('score'))
        rating = title_rating.get('rating')
        return rating

class ReviewSerializer(serializers.ModelSerializer):


    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)
    


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('text', 'pub_date', 'author', 'review')
        read_only_fields = ('author',)