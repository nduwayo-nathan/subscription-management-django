# subscriptions/models.py
from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone

class CustomUser(AbstractUser):
    # Add any additional fields you need
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField()  # Duration in months

    def __str__(self):
        return self.name

    def duration_in_days(self):
        return self.duration_months * 30  # Approximation of months to days

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use the custom user model
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def renew(self):
        """Logic to renew the subscription"""
        self.start_date = timezone.now().date()
        self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_months * 30)  # Approx. months
        self.active = True

    def cancel(self):
        """Logic to cancel the subscription"""
        self.active = False
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use the custom user model
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment {self.id} by {self.user.username}"
