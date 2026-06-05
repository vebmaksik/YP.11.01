from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views # Встроенные views для входа
from rest_framework.routers import DefaultRouter

from .views import *
from .api_views import (
    RoleViewSet, FixerProfileViewSet, CategoryViewSet,
    WorkshopViewSet, CollectionViewSet, EquipmentViewSet,
    ReviewViewSet, CartItemViewSet
)

# REST API Роутер
router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='api_role')
router.register(r'profiles', FixerProfileViewSet, basename='api_profile')
router.register(r'categories', CategoryViewSet, basename='api_category')
router.register(r'workshops', WorkshopViewSet, basename='api_workshop')
router.register(r'collections', CollectionViewSet, basename='api_collection')
router.register(r'equipment', EquipmentViewSet, basename='api_equipment')
router.register(r'reviews', ReviewViewSet, basename='api_review')
router.register(r'cart-items', CartItemViewSet, basename='api_cartitem')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Главная и О компании
    path('', home_view, name='home'),
    path('info/', info_view, name='info'),
    
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # Сессионная корзина и Заказы
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:pk>/', cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', cart_remove, name='cart_remove'),
    path('cart/order/', create_order, name='create_order'),
    
    # Снаряжение (Equipment)
    path('equipment/', EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/<int:pk>/', EquipmentDetailView.as_view(), name='equipment_detail'),
    path('equipment/create/', EquipmentCreateView.as_view(), name='equipment_create'),
    path('equipment/<int:pk>/update/', EquipmentUpdateView.as_view(), name='equipment_update'),
    path('equipment/<int:pk>/delete/', EquipmentDeleteView.as_view(), name='equipment_delete'),
    
    # Мастерские (Workshop)
    path('workshops/', WorkshopListView.as_view(), name='workshop_list'),
    path('workshops/<int:pk>/', WorkshopDetailView.as_view(), name='workshop_detail'),
    path('workshops/create/', WorkshopCreateView.as_view(), name='workshop_create'),
    path('workshops/<int:pk>/update/', WorkshopUpdateView.as_view(), name='workshop_update'),
    path('workshops/<int:pk>/delete/', WorkshopDeleteView.as_view(), name='workshop_delete'),

    # Категории (Category)
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # Профили Фиксеров (FixerProfile)
    path('fixers/', FixerProfileListView.as_view(), name='fixer_list'),
    path('fixers/<int:pk>/', FixerProfileDetailView.as_view(), name='fixer_detail'),
    path('fixers/create/', FixerProfileCreateView.as_view(), name='fixer_create'),
    path('fixers/<int:pk>/update/', FixerProfileUpdateView.as_view(), name='fixer_update'),
    path('fixers/<int:pk>/delete/', FixerProfileDeleteView.as_view(), name='fixer_delete'),

    # Отзывы (Review)
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),

    # API
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]