from django.contrib import admin
from django.urls import include, path
from bookr.views import profile
# from bookr_admin.admin import admin_site

urlpatterns = [
    path('accounts/',include(('django.contrib.auth.urls','auth',),namespace='accounts')),
    path('accounts/profile/',profile,name='profile'),
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')),
    path('filter_demo/',include('filter_demo.urls')),
    path('book_management/',include('book_management.urls')),
]