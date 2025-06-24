from django.db import models
from django.utils import timezone


class Brand(models.Model):
    name = models.CharField(max_length=100)
    daily_budget = models.FloatField()
    monthly_budget = models.FloatField()
    current_daily_spend = models.FloatField(default=0.0)
    current_monthly_spend = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()

    def is_current_hour_in_schedule(self):
        now = timezone.now()
        return self.start_hour <= now.hour < self.end_hour

    def __str__(self):
        return f"{self.start_hour}:00 - {self.end_hour}:00"


class Campaign(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="campaigns")
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    daily_spend = models.FloatField(default=0.0)
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Paused'})"

    def within_schedule(self):
        return self.schedule.is_current_hour_in_schedule() if self.schedule else True
