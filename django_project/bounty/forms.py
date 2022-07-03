from django import forms
from .models import Bounty, Images, Completion

class BountyForm(forms.ModelForm):

    title = forms.CharField(max_length=128)
 
    class Meta:
        model = Bounty
        fields = ['title', 'description', ]

class CompletionForm(forms.ModelForm):

    title = forms.CharField(max_length=128)
    latitude = forms.DecimalField()
    longitude = forms.DecimalField()
 
    class Meta:
        model = Completion
        fields = ['title', "latitude", "longitude", 'description', ]

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image', )