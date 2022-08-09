from rest_framework import viewsets
from reviews.models import *
from api.serializers import *

class ReviewViewSet(viewsets.ModelViewSet)
serializer_class = ReviewSerializer
# permission_classes = 
