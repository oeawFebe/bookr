from django.contrib.admin.apps import AdminConfig

class BookrAdminConfig(AdminConfig):
    default_site = 'bookr_admin.admin.BookrAdmin'

# from django.apps import AppConfig

#
#
# class BookrAdminConfig(AppConfig):
#     name = 'bookr_admin'
