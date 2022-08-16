from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitlesPostSerialzier, TitlesSerializer,
                             UserSerializer, SignUpSerializer, TokenRegSerializer)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet, NumberFilter)
from rest_framework import filters, mixins, permissions, viewsets, status,views
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from .permissions import AuthorPermission, AdminPermission
from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken



@permission_classes([AllowAny])
class SignUpApiView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            code = default_token_generator.make_token(user)
            send_mail('Subject here', code,'1@api.api', [request.data.get('email')],)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class TokenRegApiView(APIView):
    
    def post(self, request):
        print(f'Посмотри, какой реквест: {self.request}')
        serializer = TokenRegSerializer(data=request.data)
        print(f'Посмотри, какой сериализатор: {serializer}')
        if serializer.is_valid():
            username = serializer.data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.data.get('confirmation_code')
            if not default_token_generator.check_token(user, confirmation_code):
                message = 'Вы использовали непровиль код или время действия окончено'
                return Response({message}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)

        print(f'Посмотри: {token}')
        return Response({'token': str(token.access_token)}, status=status.HTTP_200_OK)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
    lookup_field = 'username'

    @action(methods=['patch', 'get'], detail=True, permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            print(f'Это объект me {serializer}')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminPermission]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminPermission]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [AdminPermission]
    # pagination_class = 
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        request = self.request.method
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
    serializer_class = ReviewSerializer
    permission_classes = [AuthorPermission]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    # def perform_update(self, serializer):
    #     if serializer.instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     serializer.save(author=self.request.user)

    # def perform_destroy(self, instance):
    #     if not (instance.author == self.request.user or self.request.user.is_superuser or self.request.user.is_admin or self.request.user.is_moderator):
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorPermission]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    # def perform_update(self, serializer):
    #     if not (serializer.instance.author == self.request.user or self.request.user.is_superuser or self.request.user.is_admin or self.request.user.is_moderator):
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     serializer.save()

    # def perform_destroy(self, instance):
    #     if not (instance.author == self.request.user or self.request.user.is_superuser or self.request.user.is_admin or self.request.user.is_moderator):
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     instance.delete()
