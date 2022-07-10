from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from os import path, remove

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg",upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self,**kwargs):
        max_w,max_h = 2048,2048

        super().save() #save the parent class

        pathname = self.image.path
        img = Image.open(pathname)

        if img.height > max_h or img.width > max_w:
            output_size = (max_w,max_h)
            img.thumbnail(output_size)
            img.save(pathname)