from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

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

    bounty = models.ForeignKey(Bounty,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    #coordinates
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(default="default.jpg",upload_to="bounty_images")
    date_posted = models.DateTimeField(default=timezone.now)

    class Options(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    is_completed = models.CharField(max_length=8,choices=Options.choices,default=Options.PENDING)

    def get_absolute_url(self):
        return reverse("bounty-detail",kwargs={"pk": self.bounty.id})

class Images(models.Model):

    bounty = models.ForeignKey(Bounty,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="bounty_images")

