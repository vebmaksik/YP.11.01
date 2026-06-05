from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

MAX_LENGTH = 255

class Role(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Название роли')
    clearance_level = models.PositiveIntegerField(default=1, verbose_name='Уровень допуска')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class FixerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Роль')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение профиля')
    bio = models.TextField(null=True, blank=True, verbose_name='Досье фиксера')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('fixer_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Профиль фиксера'
        verbose_name_plural = 'Профили фиксеров'


class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование категории')
    description = models.TextField(null=True, blank=True, verbose_name='Описание категории')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Workshop(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование мастерской')
    description = models.TextField(null=True, blank=True, verbose_name='Описание мастерской')
    logo = models.ImageField(upload_to='workshops/%Y/%m/%d', null=True, blank=True, verbose_name='Логотип')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('workshop_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Мастерская'
        verbose_name_plural = 'Мастерские'


class Collection(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование коллекции')
    description = models.TextField(null=True, blank=True, verbose_name='Описание коллекции')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'


class Equipment(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование снаряжения')
    description = models.TextField(null=True, blank=True, verbose_name='Описание снаряжения')
    price = models.FloatField(verbose_name='Цена (Ankh)')
    level = models.PositiveBigIntegerField(default=1, verbose_name='Уровень опасности/силы')
    color = models.CharField(max_length=MAX_LENGTH, verbose_name='Преобладающий цвет')
    photo = models.ImageField(upload_to='equipment/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления')
    is_exists = models.BooleanField(default=True, verbose_name='Доступность к заказу')

    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    workshop = models.ForeignKey(Workshop, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Мастерская')
    collection = models.ManyToManyField(Collection, verbose_name='Коллекции')

    def __str__(self):
        return f"{self.name} - {self.price} Ankh"

    def get_absolute_url(self):
        return reverse('equipment_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Позиция снаряжения'
        verbose_name_plural = 'Позиции снаряжения'


class Review(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='reviews', verbose_name='Снаряжение')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Фиксер')
    rating = models.PositiveIntegerField(default=5, verbose_name='Оценка силы (1-5)')
    comment = models.TextField(verbose_name='Комментарий фиксера')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.equipment.name}"

    def get_absolute_url(self):
        return reverse('review_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Снаряжение')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f"{self.equipment.name} (x{self.quantity}) в корзине у {self.user.username}"

    class Meta:
        verbose_name = 'Предмет в корзине'
        verbose_name_plural = 'Предметы в корзине'


# ==================== НОВЫЕ ТАБЛИЦЫ ДЛЯ ЗАКАЗОВ ====================

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('approved', 'Утвержден'),
        ('completed', 'Выполнен'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Фиксер')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус заказа')
    total_price = models.FloatField(default=0.0, verbose_name='Итоговая стоимость (Ankh)')

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Снаряжение')
    price = models.FloatField(verbose_name='Цена при оформлении')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f"{self.equipment.name} x{self.quantity} в заказе #{self.order.id}"

    class Meta:
        verbose_name = 'Предмет заказа'
        verbose_name_plural = 'Предметы заказа'