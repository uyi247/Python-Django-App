from django import forms

from main_app.models import Collection

class RatingForm(forms.ModelForm):

    class Meta:
        model = Collection
        fields = ['rating', 'review']