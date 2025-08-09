from rest_framework import permissions, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Food, Restaurant
from .serializers import FoodSerializer, RestaurantSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'address']
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return super().get_object()
        except:
            raise NotFound(detail="Restaurant not found.")

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Filter restaurants by name", type=openapi.TYPE_STRING),
        openapi.Parameter('address', openapi.IN_QUERY, description="Filter restaurants by address", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def foods(self, request, pk=None):
        restaurant = self.get_object()
        foods = restaurant.foods.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_foods = paginator.paginate_queryset(foods, request)
        serializer = FoodSerializer(paginated_foods, many=True)
        return paginator.get_paginated_response(serializer.data)


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'restaurant__name', 'featured']
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return super().get_object()
        except:
            raise NotFound(detail="Food item not found.")
        
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Filter by food name", type=openapi.TYPE_STRING),
        openapi.Parameter('restaurant__name', openapi.IN_QUERY, description="Filter by restaurant name", type=openapi.TYPE_STRING),
        openapi.Parameter('featured', openapi.IN_QUERY, description="Filter by featured status (true/false)", type=openapi.TYPE_BOOLEAN),  # new param
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
