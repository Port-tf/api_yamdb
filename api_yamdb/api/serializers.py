from rest_framework import serializers
from reviews.models import Category, Genre, Titles


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer():
    class Meta:
        model = Genre
        fields = '__all__'


class TitlesSerializer():
    class Meta:
        model = Titles
        fields = '__all__'
