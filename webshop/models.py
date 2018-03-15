from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    height = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    country = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=500)

    NO_DISCOUNT = '-'
    THREE_FOR_TWO = '3 for 2'
    TWO_FOR_1 = '2 for 1'
    SEVENTY_PERCENT = '70%'
    SIXTY_PERCENT = '60%'
    FIFTY_PERCENT = '50%'
    FORTY_PERCENT = '40%'
    THIRTY_PERCENT = '30%'
    TWENTY_PERCENT = '20%'
    TEN_PERCENT = '10%'
    FIVE_PERCENT = '5%'

    DISCOUNT_CHOICES = (
        (NO_DISCOUNT, 'no discount'),
        (THREE_FOR_TWO, '3 for 2'),
        (TWO_FOR_1, '2 for 1'),
        (SEVENTY_PERCENT, '70%'),
        (SIXTY_PERCENT, '60%'),
        (FIFTY_PERCENT, '50%'),
        (FORTY_PERCENT, '40%'),
        (THIRTY_PERCENT, '30%'),
        (TWENTY_PERCENT, '20%'),
        (TEN_PERCENT, '10%'),
        (FIVE_PERCENT, '5%')
    )

    discount = models.CharField(max_length=11, choices=DISCOUNT_CHOICES, default=NO_DISCOUNT)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, unique=True)
    quantity = models.IntegerField(max_length=100, validators=[MinValueValidator(0)])