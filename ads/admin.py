from django.contrib import admin
from .models import Brand, Campaign, Schedule


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "daily_budget", "monthly_budget")
    search_fields = ("name",)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "status", "start_date", "end_date")
    list_filter = ("status", "brand")
    search_fields = ("name",)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("campaign", "day_of_week", "start_hour", "end_hour")
    list_filter = ("day_of_week",)
