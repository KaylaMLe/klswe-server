from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "slug", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at", "-updated_at")
