from django.contrib import admin
from .models import Event, EventCompleted


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ("title", "event_manager", "start_date", "end_date")
    search_fields = (
        "title",
        "event_manager__user_profile__user__email",
        "event_manager__user_profile__user__username",
        "event_manager__user_profile__user__first_name",
        "event_manager__user_profile__user__last_name",
    )


class EventCompletedAdmin(admin.ModelAdmin):
    model = EventCompleted
    list_display = ("tourist", "event", "event_manager", "completed_at")
    search_fields = (
        "tourist__user_profile__user__email",
        "tourist__user_profile__user__username",
        "tourist__user_profile__user__first_name",
        "event__title",
        "event_manager__user_profile__user__first_name",
        "event_manager__user_profile__user__last_name",
    )


admin.site.register(Event, EventAdmin)
admin.site.register(EventCompleted, EventCompletedAdmin)
