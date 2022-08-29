from django.forms import ModelForm
from django import forms

class SearchForm(forms.Form):
    checkin = forms.DateField()
    checkout = forms.DateField()
    adults = forms.IntegerField()
    kids = forms.IntegerField()