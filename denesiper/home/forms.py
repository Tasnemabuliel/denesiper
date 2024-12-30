from django import forms
from .models import Lawyer
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = ['first_name', 'last_name', 'specialization', 'location', 'photo', 'rating', 'price_range', 'years_of_experience', 'phone_number', 'email']
    location = forms.CharField(max_length=100, required=True, label="Location")


class LawyerSearchForm(forms.Form):
    name = forms.CharField(required=False, label='Search by Name')
    specialization = forms.CharField(required=False, label='Search by Specialization')
    location = forms.CharField(required=False, label='Search by Location')
    min_rating = forms.DecimalField(required=False, max_digits=2, decimal_places=1, label='Minimum Rating')
    max_price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Maximum Price')