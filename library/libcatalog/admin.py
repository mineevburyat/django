from django.contrib import admin

# Register your models here.

from .models import Genre, Book, BookInstance, Author

#admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
admin.site.register(Book, BookAdmin)
# admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
admin.site.register(Author, AuthorAdmin)
# admin.site.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Genre, GenreAdmin)

# admin.site.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(BookInstance, BookInstanceAdmin)