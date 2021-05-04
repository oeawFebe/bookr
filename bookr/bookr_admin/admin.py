from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
# from django.contrib.auth.admin import User
class BookrAdmin(admin.AdminSite):
    site_header='Bookr Administration'
    logout_template='admin/logout.html'
    def each_context(self, request):
        context=super().each_context(request)
        context['username']=request.user.username
        return context
    def profile_view(self,request):
        request.current_app=self.name
        context=self.each_context(request)
        return TemplateResponse(request,'admin/admin_profile.html',context)
    def get_urls(self):
        urls=super().get_urls()
        url_patterns=[path('admin_profile',self.admin_view(self.profile_view)),]
        return urls+url_patterns

# admin_site=BookrAdmin(name='bookr_admin')
# admin_site.register(User)
