from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.
class Bounty(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=20,decimal_places=10)
    num_accepted = models.IntegerField(default=0)
    num_submissions = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)

    author = models.ForeignKey(User,on_delete=models.CASCADE)

    image = models.ImageField(default="default.jpg",upload_to="bounty_images")

    def __str__(self):
        return self.title

    # resolves: No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.
    def get_absolute_url(self):
        return reverse("bounty-detail",kwargs={"pk": self.pk})