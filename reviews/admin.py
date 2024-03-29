from django.contrib import admin
from reviews.models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"
    parameter_name = "potato"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "awesome")
        ]
    
    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        return reviews

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = ( "rating", "user__is_host", "room__category", "room__pet_friendly", WordFilter)