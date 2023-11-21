from django.contrib import admin
from .models import ExChanger, ExChangerAdresses

admin.site.register(ExChanger)


@admin.register(ExChangerAdresses)
class AdressesAdmin(admin.ModelAdmin):
    fields = ["user", "name", "address_1", "address_2", ("zip_code", "city"), "country", "default"]

