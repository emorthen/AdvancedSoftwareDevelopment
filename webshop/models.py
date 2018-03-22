from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=100)
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

    NO_BRAND = '-'
    APOLLO = 'APPOLLO'
    ROSCOCOSMOS = 'ROSCOCOSMOS'
    SpaceX = 'SpaceX'
    VOLVO = 'VOLVO'
    DBS = 'DBS'

    BRAND_CHOICES = (
        (NO_BRAND, '-'),
        (APOLLO, 'APOLLO'),
        (ROSCOCOSMOS, 'ROSCOCOSMOS'),
        (SpaceX, 'SpaceX'),
        (VOLVO, 'VOLVO'),
        (DBS, 'DBS')
    )

    NO_COUNTRY = '-'
    USA = 'US&A'
    RASSIA = 'Rassia'
    NORTHKOREA = 'North Korea'
    SOUTHTRONDELAG = 'South Trondelag'

    COUNTRY_CHOICES = (
        (NO_COUNTRY, '-'),
        (USA, 'US&A'),
        (RASSIA, 'Rassia'),
        (NORTHKOREA, 'North Korea'),
        (SOUTHTRONDELAG, 'South Trondelag')
    )

    brand = models.CharField(max_length=30, choices=BRAND_CHOICES, default=NO_BRAND)
    country = models.CharField(max_length=11, choices=COUNTRY_CHOICES, default=NO_COUNTRY)
    discount = models.CharField(max_length=11, choices=DISCOUNT_CHOICES, default=NO_DISCOUNT)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    ORDER_CONFIRMED = 'Order confirmed'
    ORDER_ACCEPTED = 'Order accepted'
    READY_FOR_TRANSPORTATION = 'Order ready for transportation'
    ORDER_SENT = 'Order sent'

    STATUS_CHOICES = (
        (ORDER_CONFIRMED, 'Order confirmed'),
        (ORDER_ACCEPTED, 'Order accepted'),
        (READY_FOR_TRANSPORTATION, 'Order ready for transportation'),
        (ORDER_SENT, 'Order sent')
    )
    status_field = models.CharField(max_length=30, choices=STATUS_CHOICES, default=ORDER_CONFIRMED)

    __original_status = None

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.__original_status = self.status_field

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.status_field != self.__original_status:
            send_mail(
                'Your order at SkyIsNotTheLimit has changed',
                'Hello!\n\nYour order at SkyIsNotTheLimit has changed status. '
                'Log in and see my orders for more details.',
                settings.EMAIL_HOST_USER,
                [self.user.username],
                fail_silently=False
            )

        super(Order, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_status = self.status_field

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)


class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'), on_delete=models.CASCADE,)
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
    # product as generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,)
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ('cart',)

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)

    # product
    def get_product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def set_product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk

    product = property(get_product, set_product)

