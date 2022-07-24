from django import forms
from .models import Bounty, Images, Completion
from django.core.validators import RegexValidator

class BountyForm(forms.ModelForm):

    title = forms.CharField(max_length=128)

    coordinates = forms.CharField(max_length=3, required=False,
    validators=[RegexValidator(
        '^[A-Q][1-9]+$',
        message ="Coordinates should be in form <A-Q><1-15>, ex: 'B13' \n" +
        "Read about coordinates here: https://foxhole.fandom.com/wiki/Community_Guides/Map_Guide"
    )])
 
    class Meta:
        model = Bounty
        fields = ['title', 'description', "job_type", "region", "coordinates"]

class CompletionForm(forms.ModelForm):

    title = forms.CharField(max_length=128)
 
    class Meta:
        model = Completion
        fields = ['title', 'description', ]

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image', )

class TextForm(forms.Form):
    text = forms.CharField()

    class Meta:
        fields = ["text"]