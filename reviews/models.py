from django.db import models
from common.models import CommonModel
# Create your models here.

class Review(CommonModel):

    """ Review from a User to a Room or Experience """

    user = models.ForeignKey("users.User", on_delete=models.CASCADE,related_name="reviews",)
    room = models.ForeignKey("rooms.Room", null=True, blank=True, on_delete=models.CASCADE, related_name="reviews") # Room or Experience 방을 가리키고 있는 리뷰에 접근하는 방법
    experience = models.ForeignKey("experiences.Experience", null=True, blank=True, on_delete=models.CASCADE,related_name="reviews",)
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} / {self.rating}"


