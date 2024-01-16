from django.contrib import admin
from .models import Room, Amenity
# Register your models here.

@admin.action(description="Set all prices to Zero")
def reset_prices(model_admin, request, rooms):
    # model_admin, request, QuerySet
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices, )

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

    search_fields = (
        # ^ : startwith
        # = : iexact
        #   : icontains
        # @ : search
        # foreginkey__related_fieldname 

        '^name', # 먼저 찾고
        '=price', # 그 다음 찾고
        'owner__username',

    )

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
