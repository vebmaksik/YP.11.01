from decimal import Decimal
from .models import Equipment

class Cart:
    def __init__(self, request):
        """
        Инициализируем корзину с использованием сессии Django.
        """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # Если корзины в сессии нет, создаем пустой словарь
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, equipment, quantity=1, override_quantity=False):
        """
        Добавляем товар в корзину или обновляем его количество.
        """
        equipment_id = str(equipment.id)
        if equipment_id not in self.cart:
            self.cart[equipment_id] = {
                'quantity': 0,
                'price': float(equipment.price)
            }
        
        if override_quantity:
            self.cart[equipment_id]['quantity'] = quantity
        else:
            self.cart[equipment_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как измененную для принудительного сохранения
        self.session.modified = True

    def remove(self, equipment):
        """
        Удаляем товар из корзины.
        """
        equipment_id = str(equipment.id)
        if equipment_id in self.cart:
            del self.cart[equipment_id]
            self.save()

    def clear(self):
        """
        Очищаем корзину в сессии.
        """
        if 'cart' in self.session:
            del self.session['cart']
            self.save()

    def get_total_price(self):
        """
        Подсчитываем полную стоимость товаров в корзине.
        """
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def __len__(self):
        """
        Подсчитываем количество позиций в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())