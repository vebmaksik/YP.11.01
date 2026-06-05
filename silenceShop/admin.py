from django.contrib import admin
from .models import Role, FixerProfile, Category, Workshop, Collection, Equipment, Review, CartItem

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'clearance_level')
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(FixerProfile)
class FixerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'bio_short')
    list_display_links = ('user',)
    list_filter = ('role',)
    search_fields = ('user__username', 'bio')

    def bio_short(self, obj):
        if obj.bio and len(obj.bio) > 50:
            return f"{obj.bio[:50]}..."
        return obj.bio or "Нет данных"
    bio_short.short_description = 'Краткое досье'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description_short')
    list_display_links = ('name',)
    search_fields = ('name',)

    def description_short(self, obj):
        if obj.description and len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description or "Без описания"
    description_short.short_description = 'Описание'

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description_short')
    list_display_links = ('name',)
    search_fields = ('name',)

    def description_short(self, obj):
        if obj.description and len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description or "Без описания"
    description_short.short_description = 'Описание'

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'level', 'color', 'category', 'workshop', 'is_exists')
    list_display_links = ('name',)
    list_editable = ('is_exists', 'price')
    list_filter = ('is_exists', 'category', 'workshop', 'level')
    search_fields = ('name', 'description', 'color')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipment', 'user', 'rating', 'created_at')
    list_display_links = ('equipment',)
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user__username', 'equipment__name')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'equipment', 'quantity')
    list_display_links = ('equipment',)
    list_filter = ('user',)