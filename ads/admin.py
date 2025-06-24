from django.contrib import admin
from .models import Brand, Campaign, Schedule


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "daily_budget", "monthly_budget")
    search_fields = ("name",)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "is_active", "created_at")
    list_filter = ("status", "brand")
    search_fields = ("name",)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("start_hour", "end_hour")
    list_filter = ("start_hour", "end_hour")
