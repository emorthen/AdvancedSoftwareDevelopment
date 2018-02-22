from django.db import models
from datetime import datetime

# Create your models here.


class Product(models.Model):
    # id automatically added by django
    # productID = models.CharField(max_length=10, primary_key=True)
    # category = models.ForeignKey('Catalog', related_name='products')
    category = models.ForeignKey('Catalog', related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    desription = models.TextField()
    photo = models.ImageField(upload_to='product_photo', blank=True)
    manufacturer = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Catalog(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150)
    publisher = models.CharField(max_length=300)
    description = models.TextField()
    pub_date = models.DateTimeField(default=datetime.now)


class ProductDetail(models.Model):
    #  The "ProductDetail" model represents information unique to a specific product.
    # This is a generic design that can be used to extend the information in the "Product" model with extra details.
    product = models.ForeignKey('Product', related_name='details')
    attribute = models.ForeignKey('ProductAttribute')
    value = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s: %s - %s' % (self.product, self.attribute, self.value)


class ProductAttribute(models.Model):
    # Represents a class of feature found across a set of products.
    # Does not store any data values related to the attribute, but only describes what kind of a
    # product feature we are trying to capture.
    # Possible attributes include things such as materials, colors, sizes..
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s' % self.name

# class CatalogCategory(models.Model):
#     catalog = models.ForeignKey('Catalog', related_name='categories')
#     parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
#     name = models.CharField(max_length=150)
#     description = models.TextField(blank=True)