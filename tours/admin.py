from django.contrib import admin
from .models import Tour, TouristCompletedTour


# Register your models here.
class TourAdmin(admin.ModelAdmin):
    model = Tour
    list_display = ("title", "guide", "start_date", "end_date")
    search_fields = (
        "title",
        "guide__user_profile__user__email",
        "guide__user_profile__user__username",
        "guide__user_profile__user__first_name",
        "guide__user_profile__user__last_name",
    )


class TouristCompletedTourAdmin(admin.ModelAdmin):
    model = TouristCompletedTour
    list_display = ("tourist", "tour", "guide", "completed_at")
    search_fields = (
        "tourist__user_profile__user__email",
        "tourist__user_profile__user__username",
        "tourist__user_profile__user__first_name",
        "tourist__user_profile__user__last_name",
        "tour__title",
        "guide__user_profile__user__first_name",
        "guide__user_profile__user__last_name",
    )


admin.site.register(Tour, TourAdmin)
admin.site.register(TouristCompletedTour, TouristCompletedTourAdmin)