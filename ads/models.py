from django.db import models
from django.utils import timezone
from typing import Optional

class Brand(models.Model):
    name: str = models.CharField(max_length=100)
    daily_budget: float = models.FloatField()
    monthly_budget: float = models.FloatField()
    current_daily_spend: float = models.FloatField(default=0.0)
    current_monthly_spend: float = models.FloatField(default=0.0)
    is_active: bool = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Schedule(models.Model):
    start_hour: int = models.IntegerField()
    end_hour: int = models.IntegerField()

    def is_current_hour_in_schedule(self) -> bool:
        now = timezone.now()
        return self.start_hour <= now.hour < self.end_hour

    def __str__(self) -> str:
        return f"{self.start_hour}:00 - {self.end_hour}:00"


class Campaign(models.Model):
    brand: Brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="campaigns")
    name: str = models.CharField(max_length=100)
    is_active: bool = models.BooleanField(default=True)
    daily_spend: float = models.FloatField(default=0.0)
    schedule: Optional[Schedule] = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True, blank=True)
    created_at: timezone.datetime = models.DateTimeField(auto_now_add=True

    def __str__(self) -> str:
        return f"{self.name} ({'Active' if self.is_active else 'Paused'})"

    def within_schedule(self) -> bool:
        return self.schedule.is_current_hour_in_schedule() if self.schedule else True
