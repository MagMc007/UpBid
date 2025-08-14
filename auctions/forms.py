from django import forms
from .models import Listings, Category


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter title"
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                "class": "form-control",
                "placeholder": "Describe your listing..."
            }),
            'starting_bid': forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Starting bid"
            }),
            'image_url': forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Image URL"
            }),
            'category': forms.Select(attrs={
                "class": "form-select",
            }),                                   
        }
        