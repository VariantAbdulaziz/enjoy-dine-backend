from rest_framework import serializers
from .models import Food, Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'address',
            'created_at',
            'updated_at'
        ]


class FoodSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Food
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image_url',
            'category',
            'featured',
            'restaurant',
            'restaurant_name',
            'created_at',
            'updated_at'
        ]
