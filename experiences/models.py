from django.db import models
from common.models import CommonModel

# Create your models here.


class Experience(CommonModel):

    """Experience Model Definition"""

    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    name = models.CharField(max_length=180)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    address = models.CharField(max_length=250, null=True)
    price = models.PositiveIntegerField()
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk")
    category = models.ForeignKey("categories.Category", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Perk(CommonModel):

    """WHAT IS INCLUDED ON A EXPERIENCE"""

    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, blank=True, null=True)
    explanation = models.TextField()

    def __str__(self):
        return self.name