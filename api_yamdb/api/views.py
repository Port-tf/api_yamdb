from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from reviews.models import Category, Comments, Genre, Review, Titles
from serializers import *


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = #AdminOrReadOnly
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = #AdminOrReadOnly
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = #AdminOrReadOnly
    pagination_class = ''
    filter_backends = (DjangoFilterBackend,)
    # по ТЗ (redoc) нужно фильтровать категорию и жанр по полю Slug
    # можно потестить вот так: category__slug и genre__slug
    filterset_fields = ('category', 'genre', 'name', 'year', )
    
    # def get_permissions(self):
    #     """Получение инфо о произведении. По ТЗ: Доступно без токена"""
    #     if self.action == 'retrieve':
    #         return (ReadOnly(),)  
    #         #пермишен ReadOnly по аналогии с kittygram для retrieve запросов
    #     return super().get_permissions()


    
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer()
    # permission_classes = 

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Titles, id=title_id)
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
