from io import StringIO
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from django.core.exceptions import ValidationError
from os import path



# Create your models here.
class Bounty(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=20,decimal_places=10,null=True,blank=True)
    num_submissions = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

    # resolves: No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.
    def get_absolute_url(self):
        return reverse("bounty-detail",kwargs={"pk": self.pk})

class Completion(models.Model):

    bounty = models.ForeignKey(Bounty,on_delete=models.CASCADE,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=8,decimal_places=6)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    title = models.CharField(max_length=128)
    description = models.TextField()
    rejection_reason = models.TextField(null=True)
    image = models.ImageField(default="default.jpg",upload_to="bounty_images")
    date_posted = models.DateTimeField(default=timezone.now)

    class Options(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    is_completed = models.CharField(max_length=8,choices=Options.choices,default=Options.PENDING)

    def get_absolute_url(self):
        return reverse("bounty-detail",kwargs={"pk": self.bounty.id})

    def clean(self):
        if self.latitude > 90 or self.latitude < -90:
            raise ValidationError(
                {'latitude': "Latitude must be between -90 and 90!"})

        if self.longitude > 180 or self.longitude < -180:
            raise ValidationError(
                {'longitude': "Longitude must be between -180 and 180!"})

class Images(models.Model):

    bounty = models.ForeignKey(Bounty,on_delete=models.CASCADE,null=True)
    completion = models.ForeignKey(Completion,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to="bounty_images")
    thumb = models.ImageField(upload_to="bounty_thumbs",null=True)

    def save(self,**kwargs):

        max_w,max_h = 400,400

        super().save() #save the parent class

        pathname = self.thumb.path
        spl = pathname.split(".")
        fullpath = spl[0] + "_thumb." + spl[-1]

        img = Image.open(pathname)

        if img.height > max_h or img.width > max_w:
            output_size = (max_w,max_h)
            img.thumbnail(output_size)
            img.save(fullpath)
            self.thumb.name = fullpath
            super().save()


    # def save(self,**kwargs):
    #     max_w,max_h = 2048,2048

    #     super().save() #save the parent class

    #     pathname = self.image.path
    #     img = Image.open(pathname)

    #     if img.height > max_h or img.width > max_w:
    #         output_size = (max_w,max_h)
    #         img.thumbnail(output_size)
    #         img.save(pathname)

    def delete(self,*args,**kwargs):
        storage, path = self.image.storage, self.image.path
        storage.delete(path)
    

