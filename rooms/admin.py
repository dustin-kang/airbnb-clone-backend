from django.contrib import admin
from .models import Room, Amenity
# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "country",
        "city",
        "price",
        "total_amenities",
        "rating",
        "rooms",
        "toilets",
        "pet_friendly",
        "kind",
    ]

    list_filter = (
        "name",
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_friendly",
        "kind",
        "amenities",        
    )

    # def total_amenities(self, room):
    #     return room.amenities.count()

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )
