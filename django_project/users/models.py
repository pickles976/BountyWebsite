from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from os import path, remove
from bounty.models import Team
from sorl.thumbnail import ImageField

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ImageField(upload_to="profile_pics")

    team = models.ForeignKey(Team,on_delete=models.CASCADE,null=True)

    discordname = models.CharField(max_length=40,null=True,blank=True)
    discordid = models.CharField(max_length=64,null=True,blank=True)
    verified = models.BooleanField(null=False,default=False)

    def __str__(self):
        return f"{self.user.username} Profile"