from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from webshop.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
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
            return redirect('index.html')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class ProductListView(LoginRequiredMixin, ListView):

    model = Product
    template_name = 'product-list.html'
    context_object_name = 'product-list'
    login_url = 'login'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product-details.html'
    context_object_name = 'product-details'
    login_url = 'login'

    def get_queryset(self):
        return Product.objects.all()
