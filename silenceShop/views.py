from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Equipment, Workshop, Category, FixerProfile, Review, Order, OrderItem
from .forms import EquipmentForm, WorkshopForm, CategoryForm, FixerProfileForm, ReviewForm
from .cart import Cart

# Функция-помощник для получения уровня допуска пользователя на сервере
def get_user_clearance(user):
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


# ==================== КЛАСС ПРОВЕРКИ ДОПУСКА ====================
class LevelRequiredMixin(UserPassesTestMixin):
    """
    Проверяет, соответствует ли уровень допуска пользователя требуемому уровню.
    Если уровень ниже необходимого, возвращает ошибку 403 Forbidden.
    """
    required_level = 1

    def test_func(self):
        return get_user_clearance(self.request.user) >= self.required_level

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("У вас недостаточно уровня допуска для проведения этой операции в Ателье.")
        return super().handle_no_permission()


# ==================== СТАТИЧЕСКИЕ СТРАНИЦЫ ====================
def home_view(request):
    return render(request, 'home.html')

def info_view(request):
    return render(request, 'info.html')


# ==================== АУТЕНТИФИКАЦИЯ ====================
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Регистрация прошла успешно. Добро пожаловать!")
        return valid


def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из профиля.")
    return redirect('home')


# ==================== СЕССИОННАЯ КОРЗИНА ====================
def cart_view(request):
    cart_session = request.session.get('cart', {})
    cart_items = []
    total_price = 0.0

    for eq_id, item_data in cart_session.items():
        try:
            equipment = Equipment.objects.get(pk=int(eq_id))
            item_total = item_data['price'] * item_data['quantity']
            total_price += item_total
            cart_items.append({
                'equipment': equipment,
                'quantity': item_data['quantity'],
                'price': item_data['price'],
                'total': item_total
            })
        except Equipment.DoesNotExist:
            pass

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def cart_add(request, pk):
    cart = Cart(request)
    equipment = get_object_or_404(Equipment, pk=pk)
    
    # Защитная проверка: доступен ли товар к покупке
    if not equipment.is_exists:
        messages.error(request, f"Товар '{equipment.name}' временно недоступен для добавления в корзину.")
        return redirect('equipment_detail', pk=pk)
        
    cart.add(equipment=equipment)
    messages.success(request, f"Товар '{equipment.name}' добавлен в корзину.")
    return redirect('equipment_list')


def cart_remove(request, pk):
    cart = Cart(request)
    equipment = get_object_or_404(Equipment, pk=pk)
    cart.remove(equipment)
    messages.success(request, f"Товар '{equipment.name}' удален из корзины.")
    return redirect('cart')


# ==================== ОФОРМЛЕНИЕ ЗАКАЗА ====================
@login_required(login_url='login')
def create_order(request):
    cart = Cart(request)
    
    if not cart.cart:
        messages.error(request, "Ваша корзина пуста. Невозможно оформить заказ.")
        return redirect('cart')
        
    order = Order.objects.create(
        user=request.user,
        total_price=cart.get_total_price()
    )
    
    for eq_id, item_data in cart.cart.items():
        try:
            equipment = Equipment.objects.get(pk=int(eq_id))
            OrderItem.objects.create(
                order=order,
                equipment=equipment,
                price=item_data['price'],
                quantity=item_data['quantity']
            )
        except Equipment.DoesNotExist:
            pass
            
    cart.clear()
    messages.success(request, "Ваш заказ успешно принят в обработку!")
    return render(request, 'order_success.html', {'order': order})


# ==================== 1. СНАРЯЖЕНИЕ (EQUIPMENT) ====================
class EquipmentListView(ListView):
    model = Equipment
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipments'
    ordering = ['-create_date']

class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = 'equipment/equipment_detail.html'
    context_object_name = 'equipment'

class EquipmentCreateView(LevelRequiredMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    required_level = 8 # Только максимальный допуск (Создание)

class EquipmentUpdateView(LevelRequiredMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    required_level = 4 # Средний допуск (Редактирование)

class EquipmentDeleteView(LevelRequiredMixin, DeleteView):
    model = Equipment
    template_name = 'equipment/equipment_confirm_delete.html'
    success_url = reverse_lazy('equipment_list')
    required_level = 8 # Только максимальный допуск (Удаление)


# ==================== 2. МАСТЕРСКИЕ (WORKSHOP) ====================
class WorkshopListView(ListView):
    model = Workshop
    template_name = 'workshops/workshop_list.html'
    context_object_name = 'workshops'

class WorkshopDetailView(DetailView):
    model = Workshop
    template_name = 'workshops/workshop_detail.html'
    context_object_name = 'workshop'

class WorkshopCreateView(LevelRequiredMixin, CreateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = 'workshops/workshop_form.html'
    required_level = 8

class WorkshopUpdateView(LevelRequiredMixin, UpdateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = 'workshops/workshop_form.html'
    required_level = 4

class WorkshopDeleteView(LevelRequiredMixin, DeleteView):
    model = Workshop
    template_name = 'workshops/workshop_confirm_delete.html'
    success_url = reverse_lazy('workshop_list')
    required_level = 8


# ==================== 3. КАТЕГОРИИ (CATEGORY) ====================
class CategoryListView(ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'

class CategoryCreateView(LevelRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    required_level = 8

class CategoryUpdateView(LevelRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    required_level = 4

class CategoryDeleteView(LevelRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    required_level = 8


# ==================== 4. ФИКСЕРЫ (FIXER PROFILE) ====================
class FixerProfileListView(ListView):
    model = FixerProfile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'profiles'

class FixerProfileDetailView(DetailView):
    model = FixerProfile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

class FixerProfileCreateView(LevelRequiredMixin, CreateView):
    model = FixerProfile
    form_class = FixerProfileForm
    template_name = 'profiles/profile_form.html'
    required_level = 8

class FixerProfileUpdateView(LevelRequiredMixin, UpdateView):
    model = FixerProfile
    form_class = FixerProfileForm
    template_name = 'profiles/profile_form.html'
    required_level = 4

class FixerProfileDeleteView(LevelRequiredMixin, DeleteView):
    model = FixerProfile
    template_name = 'profiles/profile_confirm_delete.html'
    success_url = reverse_lazy('fixer_list')
    required_level = 8


# ==================== 5. ОТЗЫВЫ (REVIEW) ====================
class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'
    context_object_name = 'review'

class ReviewCreateView(LevelRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    required_level = 1 # Отзывы могут оставлять любые фиксеры

class ReviewUpdateView(LevelRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    required_level = 4

class ReviewDeleteView(LevelRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')
    required_level = 8