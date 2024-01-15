from django.db import models
from common.models import CommonModel

# Create your models here.
class Room(models.Model):

    """ Room Model Definition"""

    class RoomKindChoice(models.TextChoices):
        ENTIRE_RLACE = ("entire_place", "Entire Place")
        PRIVATE_ROON = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(max_length=180, default="",)
    country = models.CharField(max_length=50, default="한국",)
    city = models.CharField(max_length=80, default="서울",)
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250,)
    pet_friendly = models.BooleanField(default=True,)
    kind = models.CharField(
        max_length=20,
        choices=RoomKindChoice.choices,
    )
    owner = models.ForeignKey("users.User", on_delete = models.CASCADE, )
    amenities = models.ManyToManyField("rooms.Amenity", )
    category = models.ForeignKey("categories.Category", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Amenity(CommonModel): # CommonModel 상속

    """ Amenity Model Definition """

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Amenities"