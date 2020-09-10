from django import forms

from main_app.models import Collection, CollectionRating

class RatingForm(forms.ModelForm):

    class Meta:
        model = Collection
        fields = ['rating', 'review']

class RatingUserForm(forms.ModelForm):

    class Meta:
        model = CollectionRating
        fields = ['rating', 'review']