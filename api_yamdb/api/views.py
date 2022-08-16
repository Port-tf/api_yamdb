from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitlePostSerialzier,
                             TitleSerializer, UserSerializer)
from api.filters import TitleFilter
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg, DecimalField
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet, NumberFilter)
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .permissions import AdminPermission, AuthorPermission



@permission_classes([AllowAny])
class SignUpApiView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            code = default_token_generator.make_token(user)
            send_mail('Subject here', code,
                      '1@api.api', [request.data.get('email')]
                      )
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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [AdminPermission]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitlePostSerialzier
        return TitleSerializer

    def get_queryset(self):
        queryset = Title.objects.all()
        if self.request.method == 'GET':
            queryset = queryset.annotate(
                rating=Avg('reviews__score', output_field=DecimalField())
            )
        return queryset


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
