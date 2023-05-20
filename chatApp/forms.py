from django import forms
from .models import Profile, Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter first name..'
    }))
    
    
    last_name = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter last name..'
    }))
    
    
    email = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'user@gmail.com'
    }))
    
    
    username = forms.CharField(label='User Name', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username..'
    }))
     
    password1 = forms.CharField(label="Enter Password", max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password'}
    ))
    
    password2 = forms.CharField(label="Confirm Password", max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password again'}
    ))
    
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
        
        
class ProfileForm(forms.ModelForm):
    age = forms.IntegerField(required=False, label="Enter Your age", widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Age in number', 'min': 18}
    ))
    picture =  forms.ImageField(required=False, label="choose a profile picture")
    
    
    class Meta:
        model = Profile
        fields = ('age', 'picture')