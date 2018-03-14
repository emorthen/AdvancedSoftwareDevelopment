from django.contrib import admin
from .models import Product, DiscountPercent

# Register your models here.
admin.site.register(Product)
admin.site.register(DiscountPercent)
