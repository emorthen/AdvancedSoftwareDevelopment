from django.conf.urls import url
from . import views

app_name ='webshop'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout_view, {'next_page': 'pages/login'}, name='logout'),
    url(r'^product/$', views.product_list_view, name='product-list'),
    url(r'^product/(?P<productID>\d+)/$', views.product_detail_view, name='product-details'),
    url(r'^cart/$', views.get_cart, name='cart'),
    url(r'^add_to_cart/(\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart/(\d+)/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^product_search_list_view/$', views.product_search_list_view, name='product_search_list_view'),
    url(r'^buy/$', views.make_purchase, name='Buy'),
]
