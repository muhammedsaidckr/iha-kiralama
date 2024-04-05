from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    username = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class RentalForm(forms.Form):
    start_date = forms.DateTimeField(label='Başlangıç Tarihi', widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(label='Bitiş Tarihi', widget=forms.TextInput(attrs={'type': 'datetime-local'}))