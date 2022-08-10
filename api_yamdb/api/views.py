from rest_framework import viewsets, filters
from reviews.models import Category, Genre, Titles
from serializers import CategorySerializer, GenreSerializer, TitlesSerializer
from django_filters.rest_framework import DjangoFilterBackend

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
