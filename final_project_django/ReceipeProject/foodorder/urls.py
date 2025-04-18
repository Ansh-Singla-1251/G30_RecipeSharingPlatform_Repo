# foodorder/urls.py
from django.urls import path
from . import views

app_name = 'foodorder'

urlpatterns = [
    path('add_to_cart/<int:recipe_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/<int:recipe_id>/', views.checkout, name='checkout'),
    path('delivery_address/', views.delivery_address, name='delivery_address'),
    path('order_review/', views.order_review, name='order_review'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('payment/', views.payment, name='payment'),
    path('thank_you/', views.thank_you, name='thank_you'),
]