from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from silenceShop.serializers import *
from .models import Role, FixerProfile, Category, Workshop, Collection, Equipment, Review, CartItem

# Функция-помощник получения допуска
def get_clearance(user):
    if not user.is_authenticated:
        return 0
    if user.is_superuser:
        return 10
    try:
        profile = user.fixerprofile
        if profile.role:
            return profile.role.clearance_level
    except Exception:
        pass
    return 1


# ==================== КАСТОМНАЯ ПАГИНАЦИЯ ====================
class ApiCustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


# ==================== КАСТОМНЫЕ ПРАВА ДОСТУПА API ====================

class IsClearance8OrReadOnly(permissions.BasePermission):
    """
    Просмотр доступен всем.
    Создание и удаление объектов разрешено только с уровнем допуска >= 8.
    Редактирование (PUT/PATCH) разрешено с уровнем допуска >= 4.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return get_clearance(request.user) >= 8

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ['PUT', 'PATCH']:
            return get_clearance(request.user) >= 4
        return get_clearance(request.user) >= 8


class IsOwnerOrClearance8(permissions.BasePermission):
    """
    Для личных данных (отзывы, корзины):
    Администраторы и уровень >= 8 могут делать все.
    Остальные пользователи — только со своими записями.
    """
    def has_object_permission(self, request, view, obj):
        if get_clearance(request.user) >= 8:
            return True
        return bool(request.user and obj.user == request.user)


# ==================== API VIEWSETS ====================

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    pagination_class = ApiCustomPagination
    permission_classes = [IsClearance8OrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class FixerProfileViewSet(viewsets.ModelViewSet):
    queryset = FixerProfile.objects.all().order_by('id')
    serializer_class = FixerProfileSerializer
    pagination_class = ApiCustomPagination
    permission_classes = [IsClearance8OrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['user__username', 'bio']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = ApiCustomPagination
    permission_classes = [IsClearance8OrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']


class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all().order_by('id')
    serializer_class = WorkshopSerializer
    pagination_class = ApiCustomPagination
    permission_classes = [IsClearance8OrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all().order_by('id')
    serializer_class = CollectionSerializer
    pagination_class = ApiCustomPagination
    permission_classes = [IsClearance8OrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all().order_by('id')
    serializer_class = EquipmentSerializer
    pagination_class = ApiCustomPagination
    permission_classes = [IsClearance8OrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description', 'color']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    pagination_class = ApiCustomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrClearance8]
    filter_backends = [SearchFilter]
    search_fields = ['comment', 'user__username', 'equipment__name']


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all().order_by('id')
    serializer_class = CartItemSerializer
    pagination_class = ApiCustomPagination
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrClearance8]
    filter_backends = [SearchFilter]
    search_fields = ['equipment__name', 'user__username']