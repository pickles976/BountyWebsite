from django.db import models
from django.contrib.auth.models import User
from bounty.models import Team
from sorl.thumbnail import ImageField

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    team = models.ForeignKey(Team,on_delete=models.CASCADE,null=True)

    discordname = models.CharField(max_length=40,null=True,blank=True)
    discordid = models.CharField(max_length=64,null=True,blank=True)

    verified = models.BooleanField(null=False,default=False)
    discordmessage = models.BooleanField(null=False,default=True)

    # discord stuff
    discordToken = models.CharField(max_length=32,null=True,blank=True)
    refreshToken = models.CharField(max_length=32,null=True,blank=True)
    dateAuthorized = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class ProfileImage(models.Model):

    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    image = ImageField(upload_to="profile_images")

    def delete(self,*args,**kwargs):
        storage, path = self.image.storage, self.image.path
        storage.delete(path)

class DailyVisit(models.Model):

    date = models.DateField(null=True,blank=True)
    numVisits = models.IntegerField(null=True)

    def __str__(self):
        return f"DATE: {self.date}  VISITS: {self.numVisits}"
