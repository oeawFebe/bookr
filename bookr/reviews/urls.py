from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from . import views, api_views

urlpatterns=[
    path("",views.index,name='index'),
    path("books/",views.book_list,name='book_list'),
    path("books/<int:pk>/", views.book_detail, name='book_detail'),
    path('books/search/',views.book_search,name='book_search'),
    path('publishers/<int:pk>/',views.publisher_edit,name='publisher_edit'),
    path('publishers/new/',views.publisher_edit,name='publisher_create'),
    path('books/<int:book_pk>/reviews/new/',views.review_edit,name='review_create'),
    path('books/<int:book_pk>/reviews/<int:review_pk>/', views.review_edit, name='review_edit'),
    path('books/<int:pk>/media/',views.book_media,name='book_media'),
    path('api/first_api_view/',api_views.first_api_view),
    path('api/all_books/', api_views.AllBooks.as_view(),name='all_books'),
    path('api/contributors/',api_views.ContributorView.as_view(),name='contributors'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)