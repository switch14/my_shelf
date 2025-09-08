# reading/admin.py
from django.contrib import admin
from .models import Book, Tag, Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year", "created_at")
    search_fields = ("title", "author")
    ordering = ("-created_at",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating", "read_date", "created_at")
    list_filter = ("rating", "read_date")
    search_fields = ("book__title", "user__username", "user__email", "comment")
    autocomplete_fields = ("book", "user", "tags")
    list_select_related = ("book", "user")
    date_hierarchy = "read_date"
    ordering = ("-created_at",)
