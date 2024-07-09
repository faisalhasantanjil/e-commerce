from rest_framework import serializers
from .models import Category, Tree, UserProfile, Order, OrderItem
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [ 'address', 'phone']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ['name', 'category', 'description', 'price', 'quantity', 'image']

'''
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'tree', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'is_paid', 'total_price', 'items']
'''

