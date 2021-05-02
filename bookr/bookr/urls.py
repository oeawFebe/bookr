from django.contrib import admin
from django.urls import include, path
from bookr.views import profile


urlpatterns = [
    path('accounts/',include(('django.contrib.auth.urls','auth',),namespace='accounts')),
    path('accounts/profile/',profile,name='profile'),
    path('admin/', admin.site.urls),
    path('', include('reviews.urls'))
]