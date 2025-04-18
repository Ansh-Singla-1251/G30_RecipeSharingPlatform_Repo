# FoodOrder/models.py
from django.db import models
from django.conf import settings
from recipes.models import Recipe

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.quantity * self.recipe.price

    class Meta:
        unique_together = ('user', 'recipe')

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.ForeignKey('DeliveryAddress', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    delivery_status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered')],
        default='PENDING'
    )

    def __str__(self):
        return f"Order {self.id} - {self.user.email} - {self.recipe.title}"

class DeliveryAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_preferred = models.BooleanField(default=False)  # Optional: Mark a preferred address

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.postal_code}"

    class Meta:
        verbose_name_plural = "Delivery Addresses"