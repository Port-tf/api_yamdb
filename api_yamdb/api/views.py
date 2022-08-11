from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend, CharFilter, NumberFilter, FilterSet
from rest_framework import filters, mixins, permissions, viewsets
#from django_filters import FilterSet
from reviews.models import Category, Comments, Genre, Review, Titles
from api.serializers import (UserSerializer, CategorySerializer, GenreSerializer,
                             TitlesSerializer, TitlesPostSerialzier, ReviewSerializer, CommentSerializer)
from users.models import User
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(methods=['patch', 'get'], detail=True)
    def me(self, request):
        user = User.objects.filter(
            username=self.request.user.username
        )
        serializer = self.get_serializer(user)
        serializer.save()
        return serializer.data


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = #AdminOrReadOnly
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = #AdminOrReadOnly
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    # filterset_fields = ('slug',)
    search_fields = ('name',)
    lookup_field = 'slug'

#Кастомный фильтр №1
class TitleFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Titles
        fields = ['name', 'category', 'genre', 'year']


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    # permission_classes = #AdminOrReadOnly
    # pagination_class = 
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        request = self.request.method
        print(f'Проверка типа реквеста:{request}')
        if request == 'POST' or request == 'PATCH' or request == 'PUT':
            return TitlesPostSerialzier
        return TitlesSerializer
    
    # def get_permissions(self):
    #     """Получение инфо о произведении. По ТЗ: Доступно без токена"""
    #     if self.action == 'retrieve':
    #         return (ReadOnly(),)  
    #         #пермишен ReadOnly по аналогии с kittygram для retrieve запросов
    #     return super().get_permissions()




    
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer()

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Titles, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(user=self.request.user, title=title)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = 

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        instance.delete()
