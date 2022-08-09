from django.core.exceptions import PermissionDenied

from rest_framework import viewsets
from reviews.models import Title, Score, Review, Comments
from api.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets





class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer()
    # permission_classes = 

def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        review = get_object_or_404(review, id=self.kwargs.get('title_id'))
        serializer.save(user=self.request.user, review=review)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.user != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(ReviewViewSet, self).perform_destroy(serializer)



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer()
    permission_classes = 

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(review, id=self.kwargs.get('review_id'))
        serializer.save(user=self.request.user, review=review)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.user != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(serializer)