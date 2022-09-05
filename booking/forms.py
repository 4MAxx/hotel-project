from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Booking


class SearchForm(forms.Form):
    checkin = forms.DateField()
    checkout = forms.DateField()
    adults = forms.IntegerField()
    kids = forms.IntegerField()


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повторите пароль')
    # first_name = forms.CharField(label='Фамилия')
    # last_name = forms.CharField(label='Имя')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'phone', 'first_name', 'last_name',)
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password',)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('checkin', 'checkout', 'adults', 'kids', 'special',)