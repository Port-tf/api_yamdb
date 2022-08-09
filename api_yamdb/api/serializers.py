from reviews.models import Score, Review, Comments, User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = ('score', 'user', 'title')
        read_only_fields = ('user',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('text', 'created', 'user', 'review')
        read_only_fields = ('user',)