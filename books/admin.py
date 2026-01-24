from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Author, Book, Dummy

# @admin.register(Author)
# class AuthorAdmin(ModelAdmin):
#     list_display = ("id", "name")
#     search_fields = ("name",)
#     list_filter = ()

# @admin.register(Book)
# class BookAdmin(ModelAdmin):
#     list_display = ("id", "title", "publication_date", "isbn", "created_at", "updated_at")
#     search_fields = ("title", "isbn")
#     list_filter = ("publication_date", "created_at")

# @admin.register(Dummy)
# class DummyAdmin(ModelAdmin):
#     list_display = ("id", "route", "slug")
#     search_fields = ("route", "slug")
#     list_filter = ()
