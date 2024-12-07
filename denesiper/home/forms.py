from django import forms
from .models import Lawyer

class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = ['first_name', 'last_name', 'specialization', 'email', 'phone_number','location', 'photo']
    location = forms.CharField(max_length=100, required=True, label="Location")


class LawyerSearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="Search by name")
    specialization = forms.CharField(max_length=100, required=False, label="Search by specialization")
    location = forms.CharField(max_length=100, required=False, label="Search by location")