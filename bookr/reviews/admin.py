from django.contrib import admin
from reviews.models import (Publisher,Contributor,Book,BookContributor,Review)

class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_filter = ('publisher', 'publication_date')
    list_display = ('title', 'isbn13','get_publisher','publication_date')
    search_fields = ('title','isbn__exact','publisher__name')
    def get_publisher(self,obj):
        return obj.publisher.name
    # def isbn13(self,obj):
    #     """
    #     '123333...' => '123-3-33-333333-3'
    #     """
    #     return f"{obj.isbn[0:3]}-{obj.isbn[3:4]}-{obj.isbn[4:6]}-{obj.isbn[6:12]}-{obj.isbn[12:13]}"





class ContributorAdmin(admin.ModelAdmin):
    list_display=('last_names','first_names')
    search_fields = ('last_names__startswith',)
    list_filter = ('last_names',)

class ReviewAdmin(admin.ModelAdmin):
    exclude=('date_edited',)

admin.site.register(Publisher)
admin.site.register(Contributor,ContributorAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review,ReviewAdmin)