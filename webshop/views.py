from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.cart import Cart
from webshop.models import Product
from functools import reduce
from django.db.models import Q
import operator


@login_required
def index(request):
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


@login_required
def add_to_cart(request, productID):
    product = Product.objects.get(id=productID)
    cart = Cart(request)
    cart.add(product, product.price, 1)
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart')


@login_required
def remove_all_from_cart(request):
    cart= Cart(request)
    cart.clear()
    return render(request,'purchase-completed.html')


def get_cart(request):
    return render(request, 'cart.html', dict(cart=Cart(request)))


def get_discounted_price(discount_string, total_price):
    discounted_price = total_price
    if '%' in discount_string:
        discount_percent = int(discount_string.split('%')[0])
        discounted_price = int(total_price) - (int(total_price) * discount_percent / 100)
    return str(discounted_price)


@login_required
def product_list_view(request):
    product_list = Product.objects.all()

    return render(request, 'product-list.html', {'product-list': product_list})


# class ProductListView(LoginRequiredMixin, ListView):
#
#     model = Product
#     template_name = 'product-list.html'
#     context_object_name = 'product-list'
#
#     def get_queryset(self):
#         return Product.objects.all()


@login_required
def product_detail_view(request, productID):
    product = Product.objects.get(id=productID)
    discounted_price = get_discounted_price(product.discount, product.price)
    return render(request, 'product-details.html', {'object': product, 'discounted_price': discounted_price})


class ProductSearchListView(ListView):
    """
    Display a Blog List page filtered by the search query.
    """
    paginate_by = 10

    def get_queryset(self):
        result = product_list_view()
        queryText = self.request.GET.get('q')
        queryMinPrice = self.request.GET.get('minprice')
        queryMaxPrice = self.request.GET.get('maxprice')
        if queryText:
            query_list = queryText.split()
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
        if queryMinPrice:
            result = result.filter(Q(price__gte=queryMinPrice))

        if queryMaxPrice:
            result = result.filter(Q(price__lte=queryMaxPrice))

        return result