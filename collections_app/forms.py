from django import forms

from collections_app.models import Collection


class CollectionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Collection
        fields = ["title", "description", "is_public"]