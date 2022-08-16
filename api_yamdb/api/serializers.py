import datetime as dt

from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import ValidationError
from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
    
    # def validate(self, data):
    #     print(self.context)
    #     author = self.context.get('request').user
    #     title_id = self.context.get('view').kwargs.get('title_id')
    #     title = get_object_or_404(Title, id=title_id)
    #     if (
    #         self.context.get('request').method == 'POST'
    #         and Review.objects.filter(title_id=title.id, author=author).exists()
    #     ):
    #         raise ValidationError('Может существовать только один отзыв!')
    #     return data    


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlePostSerialzier(serializers.ModelSerializer):
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
        model = Title
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


class TitleSerializer(serializers.ModelSerializer):
    """Сериайлайзер для всех запросов кроме POST, PUT, PATCH"""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'genre',
                  'category', 'description', 'rating'
                  )

    def get_rating(self, obj):
        """Считает средний рейтинг произведения"""
        title_rating = obj.reviews.aggregate(rating=Avg('score'))
        rating = title_rating.get('rating')
        if rating is None:
            return None
        return round(rating, 1)

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    
    def validate(self, data):
        print(self.context)
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if (
            self.context.get('request').method == 'POST'
            and Review.objects.filter(title_id=title.id, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    class Meta:
        model = Comments
        fields = ('id', 'text', 'pub_date', 'author', 'review')
        read_only_fields = ('review',)