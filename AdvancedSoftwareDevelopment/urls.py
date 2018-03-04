from django.conf.urls import include, url
from django.contrib import admin
from webshop import views
from webshop.views import ProductListView

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('', include('webshop.urls'), name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout_view, {'next_page': 'login'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^product/$', ProductListView.as_view(), name='product-list'),
    url(r'^product/(?P<productID>\d+)/$', views.product_detail_view, name='product-details'),
    url(r'^cart/$', views.get_cart, name='cart'),
    url(r'^add_to_cart/(\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart/(\d+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^buy/$',views.remove_all_from_cart,name='Buy'),
]

