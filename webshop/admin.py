from django.contrib import admin
from .models import Product, ProductAttribute, ProductDetail, Catalog

# Register your models here.
admin.site.register(Product)
admin.site.register(Catalog)
admin.site.register(ProductDetail)
admin.site.register(ProductAttribute)
