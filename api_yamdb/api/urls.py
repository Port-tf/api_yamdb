from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignUpApiView, TitleViewSet,
                       TokenRegApiView, UserViewSet)

from django.urls import include, path

from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),

    path('v1/auth/signup/', SignUpApiView.as_view(), name='signup'),
    path('v1/auth/token/', TokenRegApiView.as_view(), name='token_access'),
]
