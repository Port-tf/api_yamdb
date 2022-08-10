from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import *
from rest_framework_simplejwt.views import TokenObtainSlidingView

app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comments')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),

    # path('v1/signup/', TokenObtainSlidingView.as_view(), name='token_obtain_sliding'),
    path('v1/token/', TokenObtainSlidingView.as_view(), name='token_obtain_sliding'),
]
