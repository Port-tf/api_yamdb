from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainSlidingView


app_name = 'users'


urlpatterns = [
    path('signup/', TokenObtainSlidingView.as_view(), name='token_obtain_sliding'),
    path('token/', TokenObtainSlidingView.as_view(), name='token_obtain_sliding'),
]