from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from webshop.cart import Cart
from webshop.models import Product, Order
import webshop.models as models
from functools import reduce
from django.db.models import Q
import operator
from django.core.mail import send_mail
from django.conf import settings


@login_required
def index(request):
    return render(request, 'pages/index.html')


def logout_view(request):
    logout(request)
    return redirect('pages/login')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('webshop:index')
    else:
        form = UserCreationForm()
    return render(request, 'pages/signup.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.stock >= 1:
        cart = Cart(request)
        cart.add(product, product.price, 1)
        product.errortext = ''
        product.save()
        return redirect('webshop:cart')
    product.errortext = 'Not enough items available in stock!'
    product.save()
    return redirect('webshop:product-list')


@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('webshop:cart')


@login_required
def add_order(request):
    products = dict(cart=Cart(request))['cart'].get_product()
    for product in products:
        order = models.Order(product=product, user=request.user)
        order.save()


@login_required
def order_view(request):
    current_user = request.user
    order_list = Order.objects.filter(user=current_user)
    return render(request, 'pages/order-list.html', {'order_list': order_list})


@login_required
def purchase(request):
    cart = Cart(request)
    add_order(request)
    products_in_cart = cart.get_products()
    for item in products_in_cart:
        product = Product.objects.get(id=item.product.id)
        product.stock = product.stock - item.quantity
        product.save()
    cart.clear()
    send_mail(
        'Your purchase at SkyIsNotTheLimit',
        'Hello!\n\nYour purchase at SkyIsNotTheLimit is confirmed. Se my orders for more details.',
        settings.EMAIL_HOST_USER,
        [request.user.username],
        fail_silently=False
    )
    return render(request, 'pages/purchase-completed.html')


@login_required
def increase_in_cart(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    quantity = int(quantity) + 1
    if product.stock >= quantity:
        cart = Cart(request)
        cart.update(product, quantity, product.price)
    return redirect('webshop:cart')


@login_required
def decrease_in_cart(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    quantity = int(quantity) - 1
    cart.update(product, quantity, product.price)
    return redirect('webshop:cart')


@login_required
def get_cart(request):
    return render(request, 'pages/cart.html', dict(cart=Cart(request)))


@login_required
def product_list_view(request):
    product_list = Product.objects.all()

    return render(request, 'pages/product-list.html', {'product_list': product_list})


@login_required
def product_detail_view(request, productID):
    product = Product.objects.get(id=productID)
    discounted_price = product.get_discounted_price()
    return render(request, 'pages/product-details.html', {'product': product, 'discounted_price': discounted_price})


@login_required
def product_search_list_view(request):
    result = Product.objects.all()
    query_text = request.GET.get('q')
    query_min_price = request.GET.get('minprice')
    query_max_price = request.GET.get('maxprice')
    if query_text:
        query_list = query_text.split()
        result = result.filter(
            reduce(operator.and_,
                   (Q(brand__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(description__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(name__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(country__icontains=q) for q in query_list))
        )
    if query_min_price:
        result = result.filter(Q(price__gte=query_min_price))

    if query_max_price:
        result = result.filter(Q(price__lte=query_max_price))

    return render(request, 'pages/product-list.html', {'product_list': result})
