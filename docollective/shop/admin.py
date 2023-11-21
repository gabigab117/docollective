from django.contrib import admin
from .models import Color, Garment, Cart, Order

admin.site.register(Color)
admin.site.register(Cart)


@admin.register(Garment)
class GarmentAdmin(admin.ModelAdmin):
    list_display = ["description", "user", "published", "activate", "bought"]
    list_editable = ["activate"]
    list_display_links = ["description"]
    list_filter = ["activate", "bought"]
    search_fields = ["description__icontains", "user__email__icontains"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "ordered", "ordered_date", "validation", "reference"]
    list_editable = ["validation"]
    list_filter = ["ordered", "validation"]
    search_fields = ["user", "reference"]
