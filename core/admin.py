from django.contrib import admin
from core.models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
)



# Regestering in Admin Page

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone','city', 'locality', 'zipcode', 'state']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'brand', 'selling_price', 'discounted_price', 'category', 'product_image']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderplacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']




