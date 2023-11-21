from django.contrib import admin
from .models import ExChanger, ExChangerAdresses


@admin.register(ExChanger)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "is_active", "is_superuser"]
    list_editable = ["is_active", "is_superuser"]
    list_filter = ["is_active"]
    search_fields = ["first_name", "last_name"]


@admin.register(ExChangerAdresses)
class AdressesAdmin(admin.ModelAdmin):
    fields = ["user", "name", "address_1", "address_2", ("zip_code", "city"), "country", "default"]

