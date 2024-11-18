from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Payment

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration_months', 'duration_in_days']  # Add duration_in_days method to list_display

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'start_date', 'end_date', 'active']
    list_filter = ['active', 'plan', 'start_date']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'amount', 'date']
    list_filter = ['date', 'subscription']

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Payment, PaymentAdmin)
