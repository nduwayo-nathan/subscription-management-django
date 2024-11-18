from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.utils import timezone
from .models import SubscriptionPlan, Subscription, Payment
from .forms import UserRegistrationForm, SubscriptionPlanForm, SubscriptionForm
from django.contrib import messages


# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'subscriptions/login.html'

    def get_success_url(self):
        return reverse('dashboard')


# Dashboard View
@login_required
def dashboard(request):
    user_subscription = Subscription.objects.filter(user=request.user).first()
    if user_subscription:
        context = {'user_subscription': user_subscription}
    else:
        context = {'error_message': 'You have not subscribed yet. Please choose a plan.'}
    return render(request, 'dashboard.html', context)


# User Registration
def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please select a subscription plan.')
            return redirect('subscription_plans')
    else:
        form = UserRegistrationForm()
    return render(request, 'subscriptions/register.html', {'form': form})


# View Subscription Plans
def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/plans.html', {'plans': plans})


# Subscribe to a Plan
def subscribe(request, plan_id):
    plan = SubscriptionPlan.objects.get(id=plan_id)
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.plan = plan
            subscription.save()
            messages.success(request, f'Successfully subscribed to {plan.name} plan!')
            return redirect('view_subscriptions')
    else:
        form = SubscriptionForm(initial={'plan': plan, 'user': request.user})
    return render(request, 'subscriptions/subscribe.html', {'form': form, 'plan': plan})


# View Active Subscriptions
def view_subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user, active=True, end_date__gte=timezone.now().date())
    return render(request, 'subscriptions/view_subscriptions.html', {'subscriptions': subscriptions})


# Manage Subscription (Renew, Cancel, Upgrade)
def manage_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'renew':
            subscription.renew()  # Add logic to renew subscription
            subscription.save()
            messages.success(request, 'Subscription has been successfully renewed!')
        elif action == 'cancel':
            subscription.cancel()  # Add logic to cancel subscription
            subscription.save()
            messages.success(request, 'Subscription has been successfully canceled!')
        elif action == 'upgrade':
            # Upgrade logic - user selects new plan
            new_plan = SubscriptionPlan.objects.get(id=request.POST.get('new_plan_id'))
            subscription.plan = new_plan
            subscription.save()
            messages.success(request, f'Successfully upgraded to the {new_plan.name} plan!')
        
        return redirect('view_subscriptions')

    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/manage_subscription.html', {'subscription': subscription, 'plans': plans})


# Payment History
def payment_history(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'subscriptions/payment_history.html', {'payments': payments})


# Upcoming Renewals
def upcoming_renewals(request):
    subscriptions = Subscription.objects.filter(user=request.user, active=True, end_date__gte=timezone.now().date())
    upcoming_renewals = []
    for sub in subscriptions:
        renewal_date = sub.end_date + timezone.timedelta(days=1)  # Example: renew 1 day after end_date
        upcoming_renewals.append({
            'plan': sub.plan.name,
            'renewal_date': renewal_date,
        })
    return render(request, 'subscriptions/upcoming_renewals.html', {'upcoming_renewals': upcoming_renewals})


# Update Account Info
def update_account_info(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account information updated successfully!')
            return redirect('dashboard')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'subscriptions/update_account_info.html', {'form': form})

