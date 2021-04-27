from django.apps import AppConfig
from django.contrib.admin.apps import SimpleAdminConfig

class ReviewsConfig(AppConfig):
    name = 'reviews'

class ReviewsAdminConfig(SimpleAdminConfig):
    default_site = 'admin.BookrAdminSite'