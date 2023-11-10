from django.contrib import admin
from .models import Color, Garment, Cart, Order

admin.site.register(Color)
admin.site.register(Cart)
admin.site.register(Order)


@admin.register(Garment)
class GarmentAdmin(admin.ModelAdmin):
    list_display = ["description", "user", "published", "activate", "bought"]
    list_editable = ["activate"]
    list_display_links = ["description"]
    list_filter = ["activate", "bought"]
