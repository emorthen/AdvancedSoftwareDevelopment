from django.db import models

# Create your models here.

class Product(models.Model):
    # id automatically added by django
    # productID = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    desription = models.CharField(max_length=500)
    price = models.IntegerField()
