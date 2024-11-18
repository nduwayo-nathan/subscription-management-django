# subscriptions/urls.py
from django.urls import path
from .views import CustomLoginView, register_user, subscription_plans, subscribe, view_subscriptions, manage_subscription, payment_history, upcoming_renewals, update_account_info,dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),   
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/register/', register_user, name='register'),
    path('subscription_plans/', subscription_plans, name='subscription_plans'),
    path('subscribe/<int:plan_id>/', subscribe, name='subscribe'),
    path('view_subscriptions/', view_subscriptions, name='view_subscriptions'),
    path('manage_subscription/<int:subscription_id>/', manage_subscription, name='manage_subscription'),
    path('payment_history/', payment_history, name='payment_history'),
    path('upcoming_renewals/', upcoming_renewals, name='upcoming_renewals'),
    path('update_account_info/', update_account_info, name='update_account_info'),
]
