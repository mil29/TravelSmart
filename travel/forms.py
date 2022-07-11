from django import forms
from travel.models import RecentSearches
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.ModelForm):
    destination = forms.CharField(max_length=100,label="",
                           widget= forms.TextInput
                           (attrs={'id':'destination_input', 'placeholder': 'Start typing....'}))
    
    
    class Meta:
        model = RecentSearches
        fields = ['destination']

        


        
