from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male") # 값, 표시값
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "usd", "Dollar" # 반드시 괄호가 필요없다

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    avatar = models.ImageField(blank=True) # 기본적으로 필수 이므로 blank=True를 해야 필수가 아니게 된다.
    name = models.CharField(max_length=150, default="",)
    is_host = models.BooleanField(null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices,)
    language = models.CharField(max_length=2, choices=LanguageChoices,)
    currency = models.CharField(max_length=5, choices=CurrencyChoices,)