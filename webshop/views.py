from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.cart import Cart
from webshop.models import Product

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def add_to_cart(request, productID):
    product = Product.objects.get(id=productID)
    cart = Cart(request)
    cart.add(product, product.price, 1)
    return redirect('cart')


def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart')


def get_cart(request):
    return render(request, 'cart.html', dict(cart=Cart(request)))


def get_discounted_price(discount_string, total_price):
    print('calculating discounted price')
    discounted_price = total_price
    if '%' in discount_string:
        discount_percent = int(discount_string.split('%')[0])
        discounted_price = int(total_price) * discount_percent / 100
    return str(discounted_price)


class ProductListView(LoginRequiredMixin, ListView):

    model = Product
    template_name = 'product-list.html'
    context_object_name = 'product-list'
    login_url = 'login'

    def get_queryset(self):
        return Product.objects.all()


def product_detail_view(request, productID):
    if not request.user.is_authenticated:
        return redirect('login')
    product = Product.objects.get(id=productID)
    discounted_price = get_discounted_price(product.discount, product.price)
    return render(request, 'product-details.html', {'object': product, 'discounted_price': discounted_price})

