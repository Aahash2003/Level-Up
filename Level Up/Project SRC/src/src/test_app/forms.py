from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'name', 'email', 'gender', 'age', 'height', 'weight']
