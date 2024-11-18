from django import forms
from django.contrib.auth import get_user_model
from .models import Subscription, SubscriptionPlan

CustomUser = get_user_model()  # Dynamically get the custom user model

class AccountInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Use CustomUser model instead of 'user'
        fields = ['email', 'first_name', 'last_name', 'phone_number']  # Directly use phone_number

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'price', 'duration_months']
        
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['plan', 'user', 'start_date', 'end_date', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['plan'].widget = forms.HiddenInput()
