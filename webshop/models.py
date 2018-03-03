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
    #productID = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    height = models.PositiveIntegerField()
    country = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    description = models.CharField(max_length=500)

    NO_DISCOUNT = 'NON'
    THREE_FOR_TWO = '3F2'
    TWO_FOR_1 = '2F1'
    SEVENTY_PERCENT = 'SEV'
    SIXTY_PERCENT = 'SIX'
    FIFTY_PERCENT = 'FIF'
    FORTY_PERCENT = 'FOR'
    THIRTY_PERCENT = 'THI'
    TWENTY_PERCENT = 'TWE'
    TEN_PERCENT = 'TEN'
    FIVE_PERCENT = 'FIV'

    DISCOUNT_CHOICES = (
        (NO_DISCOUNT, 'no discount'),
        (THREE_FOR_TWO, '3 for 2'),
        (TWO_FOR_1, '2 for 1'),
        (SEVENTY_PERCENT, '70 %'),
        (SIXTY_PERCENT, '60 %'),
        (FIFTY_PERCENT, '50 %'),
        (FORTY_PERCENT, '40 %'),
        (THIRTY_PERCENT, '30 %'),
        (TWENTY_PERCENT, '20 %'),
        (TEN_PERCENT, '10 %'),
        (FIVE_PERCENT, '5 %')
    )

    discount = models.CharField(max_length=3, choices=DISCOUNT_CHOICES, default=NO_DISCOUNT)

    #objects = ItemManager()
