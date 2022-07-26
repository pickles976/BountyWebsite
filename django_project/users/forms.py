from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ProfileImage

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):

    discordmessage = forms.BooleanField(label='Allow Discord Messages',required=False)    

    class Meta: 
        model = Profile
        fields = ["team","discordmessage"]

class ProfileImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image', required=False)    
    class Meta:
        model = ProfileImage
        fields = ('image', )