from django import forms
from .models import Listings


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
