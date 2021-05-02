from django.contrib import admin
# from django.contrib.auth.admin import User
class BookrAdmin(admin.AdminSite):
    site_header='Bookr Administration'
    logout_template='admin/logout.html'
# admin_site=BookrAdmin(name='bookr_admin')
# admin_site.register(User)
