
from django.contrib import admin
from .models import Product, CartItem#, ProductImage
# Register your models here.

#admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')

admin.site.register(CartItem)
