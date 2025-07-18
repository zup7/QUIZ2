# portfolio/forms.py
from django import forms
from .models import Portfolio
from django.contrib.auth.models import User

class PortfolioAdminForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False, label="User First Name")
    last_name = forms.CharField(max_length=150, required=False, label="User Last Name")

    class Meta:
        model = Portfolio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if the instance exists AND has a user associated before accessing user fields
        if self.instance and hasattr(self.instance, 'user') and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        # Important: For new instances, the 'user' field will be a dropdown.
        # Ensure that if it's a new instance, these fields are not populated prematurely.


    def save(self, commit=True):
        portfolio = super().save(commit=False)

        # Ensure that portfolio.user exists before trying to save first_name/last_name
        # The 'user' field is a dropdown on the admin form, and will be set after saving the Portfolio
        # So we should only update user details if a user is *already* associated.
        if portfolio.user: # This will be True for existing portfolios, or after a new portfolio is saved with a user.
            user = portfolio.user
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.save()

        if commit:
            portfolio.save()
        return portfolio