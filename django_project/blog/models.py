from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # resolves: No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.
    def get_absolute_url(self):
        return reverse("post-detail",kwargs={"pk": self.pk})