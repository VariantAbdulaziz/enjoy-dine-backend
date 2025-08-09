from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodViewSet, RestaurantViewSet

router = DefaultRouter()
router.register(r'foods', FoodViewSet, basename='food')
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')

urlpatterns = [
    path('', include(router.urls)),
]
