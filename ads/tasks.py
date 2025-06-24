
from celery import shared_task
from django.utils import timezone
from .models import Campaign, Brand


@shared_task
def enforce_budget_limits() -> None:
    """
    Disable campaigns if their brand's daily/monthly spend exceeds the budget.
    """
    for campaign in Campaign.objects.select_related('brand'):
        brand = campaign.brand
        if (brand.current_daily_spend > brand.daily_budget or
            brand.current_monthly_spend > brand.monthly_budget):
            if campaign.is_active:
                campaign.is_active = False
                campaign.save()


@shared_task
def enforce_dayparting() -> None:
    """
    Enable/disable campaigns based on their dayparting schedule and budget.
    """
    now_hour = timezone.now().hour

    for campaign in Campaign.objects.select_related('brand', 'schedule'):
        brand = campaign.brand
        schedule = campaign.schedule

        in_schedule = schedule and schedule.start_hour <= now_hour < schedule.end_hour
        budget_ok = (
            brand.current_daily_spend <= brand.daily_budget and
            brand.current_monthly_spend <= brand.monthly_budget
        )

        if in_schedule and budget_ok:
            if not campaign.is_active:
                campaign.is_active = True
                campaign.save()
        else:
            if campaign.is_active:
                campaign.is_active = False
                campaign.save()


@shared_task
def reset_daily_spending() -> None:
    """
    Resets daily spend for all brands and campaigns.
    Reactivates campaigns if within schedule and under budget.
    """
    for brand in Brand.objects.all():
        brand.current_daily_spend = 0.0
        brand.save()

    for campaign in Campaign.objects.select_related('brand', 'schedule'):
        campaign.daily_spend = 0.0
        if campaign.schedule:
            now_hour = timezone.now().hour
            in_schedule = campaign.schedule.start_hour <= now_hour < campaign.schedule.end_hour
        else:
            in_schedule = True

        budget_ok = (
            campaign.brand.current_daily_spend <= campaign.brand.daily_budget and
            campaign.brand.current_monthly_spend <= campaign.brand.monthly_budget
        )

        if in_schedule and budget_ok:
            campaign.is_active = True
        campaign.save()


@shared_task
def reset_monthly_spending() -> None:
    """
    Resets monthly spend for all brands.
    """
    for brand in Brand.objects.all():
        brand.current_monthly_spend = 0.0
        brand.save()
