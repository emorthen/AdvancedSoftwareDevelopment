from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from webshop.cart import Cart
from webshop.models import Product
from functools import reduce
from django.db.models import Q
import operator


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
    cart = Cart(request)
    cart.add(product, product.price, 1)
    return redirect('webshop:cart')


@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('webshop:cart')


@login_required
def make_purchase(request):
    cart = Cart(request)
    products_in_cart = cart.get_products()
    for item in products_in_cart:
        product = Product.objects.get(id=item.product.id)
        product.stock = product.stock - item.quantity
        product.save()
    cart.clear()
    return render(request, 'pages/purchase-completed.html')

@login_required
def increase_in_cart(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    quantity = int(quantity) + 1
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


def get_discounted_price(discount_string, total_price):
    discounted_price = total_price
    if '%' in discount_string:
        discount_percent = int(discount_string.split('%')[0])
        discounted_price = int(total_price) - (int(total_price) * discount_percent / 100)
    return discounted_price


@login_required
def product_list_view(request):
    product_list = Product.objects.all()

    return render(request, 'pages/product-list.html', {'product_list': product_list})


@login_required
def product_detail_view(request, productID):
    product = Product.objects.get(id=productID)
    discounted_price = get_discounted_price(product.discount, product.price)
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
