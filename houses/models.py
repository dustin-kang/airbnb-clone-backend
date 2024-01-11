from django.db import models

# Create your models here.
class House(models.Model):
    
    """
    Model Deifinition for Houses
    """
    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField(verbose_name = "Price?", help_text="Positive number only")
    decription = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(default=True, help_text="Does this house allows pets?", verbose_name="Pets Allowed?")
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name