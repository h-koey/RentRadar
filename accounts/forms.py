from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserPreferences


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        field_classes = {"username": forms.CharField, "email": forms.EmailField}


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        exclude = ("user",)
        widgets = {
            "budget": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "min_bedrooms": forms.NumberInput(attrs={"min": "0"}),
            "min_bathrooms": forms.NumberInput(attrs={"min": "0"}),
        }
