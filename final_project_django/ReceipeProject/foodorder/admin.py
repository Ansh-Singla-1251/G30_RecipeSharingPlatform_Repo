# FoodOrder/admin.py
from django.contrib import admin
from .models import Cart, DeliveryAddress, Order

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'quantity', 'get_total_price', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'recipe__title')

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'state', 'postal_code', 'country', 'created_at')
    list_filter = ('user', 'country', 'created_at')
    search_fields = ('user__username', 'address_line1', 'city', 'state', 'postal_code', 'country')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'quantity', 'total_price', 'delivery_address', 'created_at', 'payment_status', 'delivery_status')
    list_filter = ('user', 'payment_status', 'delivery_status', 'created_at')
    search_fields = ('user__username', 'recipe__title')