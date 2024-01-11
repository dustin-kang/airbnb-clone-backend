from django.contrib import admin
from .models import House
# Register your models here.

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    
    fields = (
        "name",
        "price_per_night",
        "address",
        "pets_allowed"
    )
    # Colums showing admin page
    list_display = [
        "name",
        "price_per_night",
        "address",
        "pets_allowed"
    ]
    list_display_links = ["address"]
    list_editable = ["pets_allowed"]

    list_filter = ["price_per_night", "pets_allowed"]
    search_fields = ["address__startswith"]