from django import forms
from .models import Bounty, Images

class BountyForm(forms.ModelForm):

    title = forms.CharField(max_length=128)
    description = forms.CharField(max_length=1024, label="Description")
 
    class Meta:
        model = Bounty
        fields = ['title', 'description', ]
 
 
class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image', )