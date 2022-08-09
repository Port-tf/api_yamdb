from rest_framework import serializers
from reviews.models import Category, Genre, Titles


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
        fields = '__all__'
