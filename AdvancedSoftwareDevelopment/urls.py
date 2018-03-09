from django.conf.urls import include, url
from django.contrib import admin
from webshop import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')), 
    url('', include('webshop.urls', namespace='webshop')),
    url(r'^admin/', admin.site.urls),
    

]
