from django.db import models
from datetime import datetime

# Create your models here.

class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

class Product(models.Model):
    # id automatically added by django
    productID = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    height = models.PositiveIntegerField()
    country = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    description = models.CharField(max_length=500)

    #objects = ItemManager()
