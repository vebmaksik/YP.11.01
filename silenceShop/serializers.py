from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, FixerProfile, Category, Workshop, Collection, Equipment, Review, CartItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'clearance_level']


class FixerProfileSerializer(serializers.ModelSerializer):
    # Вложенный вывод данных о пользователе и его роли (только для чтения)
    user_details = UserSerializer(source='user', read_only=True)
    role_details = RoleSerializer(source='role', read_only=True)

    class Meta:
        model = FixerProfile
        fields = ['id', 'user', 'user_details', 'role', 'role_details', 'avatar', 'bio']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ['id', 'name', 'description', 'logo']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'description']


class EquipmentSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    workshop_details = WorkshopSerializer(source='workshop', read_only=True)

    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'description', 'price', 'level', 'color', 
            'photo', 'create_date', 'is_exists', 'category', 'category_details', 
            'workshop', 'workshop_details', 'collection'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    equipment_details = EquipmentSerializer(source='equipment', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'equipment', 'equipment_details', 'user', 'user_details', 'rating', 'comment', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    equipment_details = EquipmentSerializer(source='equipment', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'user_details', 'equipment', 'equipment_details', 'quantity']