from io import StringIO
from secrets import choice
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from django.core.exceptions import ValidationError
from os import path
from bounty.utils import get_region_mappings, get_names_with_coords, grid_to_coords
from users.models import User
import json

class Team(models.Model):

    class Factions(models.TextChoices):
        COLONIAL = "COLONIAL", "Colonial"
        WARDEN = "WARDEN", "Warden"

    team = models.CharField(max_length=8,choices=Factions.choices,default=Factions.COLONIAL)

    def __str__(self):
        return self.team

class War(models.Model):

    warNumber = models.IntegerField()
    winner = models.CharField(max_length=32,null=True)
    startTime = models.IntegerField(null=True,blank=True)
    endTime = models.IntegerField(null=True,blank=True)

# Create your models here.
class Bounty(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=20,decimal_places=10,null=True,blank=True)
    num_submissions = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    team = models.ForeignKey(Team,on_delete=models.CASCADE,null=True)

    class Regions(models.TextChoices):
        ACRITHIA = "ACRITHIA", "Acrithia"
        ALLODS = "ALLODS", "Allod's Bight"
        ASHFIELDS = "ASHFIELDS", "Ash Fields"
        BASIN = "BASIN", "Basin Sionnach"  
        CALLAHAN = "CALLAHAN", "Callahan's Passage"
        CALLUMS = "CALLUMS", "Callum's Cape"
        CLANSHEAD = "CLANSHEAD", "Clanshead Valley"
        ENDLESS = "ENDLESS", "Endless Shore"  
        FARRANAC = "FARRANAC", "Farranac Coast"
        FISHERMANS = "FISHERMANS", "Fisherman's Row"  
        GODCROFTS = "GODCROFTS", "Godcrofts"
        GREATMARCH = "GREATMARCH", "Great March"
        HOWL = "HOWL", "Howl County"
        KALOKAI = "KALOKAI", "Kalokai"
        LOCH = "LOCH", "Loch Mór"
        MARBAN = "MARBAN", "Marban Hollow"
        MORGENS = "MORGENS", "Morgen's Crossing"
        NEVISH = "NEVISH", "Nevish Line"
        ORIGIN = "ORIGIN", "Origin"
        REACHING = "REACHING", "Reaching Trail"
        REDRIVER = "REDRIVER", "Red River"
        SHACKLED = "SHACKLED", "Shackled Chasm"
        SPEAKING = "SPEAKING", "Speaking Woods"
        STONECRADLE = "STONECRADLE", "Stonecradle"
        TEMPEST = "TEMPEST", "Tempest Island"
        TERMINUS = "TERMINUS", "Terminus"
        DEADLANDS = "DEADLANDS", "The Deadlands"
        DROWNED = "DROWNED", "The Drowned Vale"
        FINGERS = "FINGERS", "The Fingers"
        HEARTLANDS = "HEARTLANDS", "The Heartlands"
        LINN = "LINN", "The Linn of Mercy"
        MOORS = "MOORS", "The Moors"
        OARBREAKER = "OARBREAKER", "The Oarbreaker Isles"
        UBMRAL = "UMBRAL", "Umbral Wildwood"
        VIPER = "VIPER", "Viper Pit"
        WEATHERED = "WEATHERED", "Weathered Expanse"
        WESTGATE = "WESTGATE", "Westgate"

    region = models.CharField(max_length=32,choices=Regions.choices,default=Regions.ASHFIELDS)

    coordinates = models.CharField(max_length=3,null=True,blank=True)

    class JobType(models.TextChoices):
        LOGI = "LOGI", "Logistics"
        DEMO = "DEMO", "Demolition"
        PARTISAN = "PARTISAN", "Partisan"
        CONSTRUCTION = "CONSTRUCTION", "Construction"
        COMBAT = "COMBAT", "Combat"
        OTHER = "OTHER", "Other"

    job_type = models.CharField(max_length=12,choices=JobType.choices,default=JobType.OTHER)

    war = models.ForeignKey(War,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("bounty-detail",kwargs={"pk": self.pk})

    # Get the coordinates from the grid square
    def get_coordinates(self):

        base_coords = get_region_mappings()[self.region]

        if self.coordinates and int(self.coordinates[1:]) < 16:
            offset = grid_to_coords(self.coordinates)
            base_coords[0] += offset[0]
            base_coords[1] += offset[1]

        return json.dumps(base_coords)

    # return a dictionary of hex names with coordinates
    def get_names(self):
        return json.dumps(get_names_with_coords())

# Acceptance object tying a user to a bounty
class Acceptance(models.Model):

    bounty = models.ForeignKey(Bounty,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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

    team = models.ForeignKey(Team,on_delete=models.CASCADE,null=True)

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

    def delete(self,*args,**kwargs):
        storage, path = self.image.storage, self.image.path
        storage.delete(path)

