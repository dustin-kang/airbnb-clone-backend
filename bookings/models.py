from django.db import models
from common.models import CommonModel 
# Create your models here.

class Booking(CommonModel):

    """ Booking Model Definition """

    class BookingKindChoice(models.TextChoices):

        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"
    
    kind = models.CharField(max_length=15, choices=BookingKindChoice.choices)
    user = models.ForeignKey(
        "users.User",
        on_delete = models.CASCADE,
        related_name = "bookings",
    )
    room = models.ForeignKey(
        "rooms.Room",
        null = True,
        blank = True,
        on_delete=models.SET_NULL,
        related_name = "bookings",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name = "bookings",
    )
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    experience_time = models.DateTimeField(null=True, blank=True)
    guests = models.PositiveIntegerField()


    def __str__(self) -> str:
        return f"{self.kind.title()} Booking for {self.user}"

