from django.contrib import admin

from .models import Event, Member, Participation, Sport, SportGroup, Testimonial


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "group_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "city",
        "level",
        "participation_count",
        "connection_count",
    )
    list_filter = ("level", "favorite_sports")
    search_fields = ("name", "email", "city")
    filter_horizontal = ("favorite_sports", "connections")


@admin.register(SportGroup)
class SportGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "sport", "neighborhood", "schedule", "is_free", "member_count")
    list_filter = ("sport", "is_free")
    search_fields = ("name", "neighborhood")
    filter_horizontal = ("members",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "sport", "date", "time_label", "location")
    list_filter = ("sport",)
    date_hierarchy = "date"
    search_fields = ("title", "location")
    filter_horizontal = ("attendees",)


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("member", "sport", "event", "group", "date")
    list_filter = ("sport", "date")
    search_fields = ("member__name",)
    autocomplete_fields = ("member", "sport")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("member", "sport")
    search_fields = ("member__name", "quote")
