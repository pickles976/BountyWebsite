from amqp import Channel
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from bounty.utils import get_region_mappings, get_names_with_coords, grid_to_coords
import json
from sorl.thumbnail import ImageField

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
    startTime = models.BigIntegerField(null=True,blank=True)
    endTime = models.BigIntegerField(null=True,blank=True)

# Create your models here.
class Bounty(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField()
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
        NONE = "NONE", "None"

    region = models.CharField(max_length=32,choices=Regions.choices,default=Regions.NONE)

    coordinates = models.CharField(max_length=3,null=True,blank=True)

    class JobType(models.TextChoices):
        LOGI = "LOGI", "Logistics"
        DEMOLITION = "DEMOLITION", "Demolition"
        PARTISAN = "PARTISAN", "Partisan"
        CONSTRUCTION = "CONSTRUCTION", "Construction"
        COMBAT = "COMBAT", "Combat"
        REFUEL = "REFUEL", "Refuel"
        OTHER = "OTHER", "Other"

    jobtype = models.CharField(max_length=12,choices=JobType.choices,default=JobType.OTHER)

    war = models.ForeignKey(War,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("bounty-detail",kwargs={"pk": self.pk})

    # Get the coordinates from the grid square
    def get_coordinates(self):

        if self.region != "NONE":

            base_coords = get_region_mappings()[self.region]

            if self.coordinates and int(self.coordinates[1:]) < 16:
                offset = grid_to_coords(self.coordinates)
                base_coords[0] += offset[0]
                base_coords[1] += offset[1]

            return json.dumps(base_coords)

        return [0,0]

    # return a dictionary of hex names with coordinates
    def get_names(self):
        return json.dumps(get_names_with_coords())

    def get_age(self):
        
        diff = timezone.now() - self.date_posted

        if diff.days > 0:
            return f"Posted {diff.days} days ago "
        elif diff.seconds > 3600:
            return f"Posted {int(diff.seconds / 3600)} hours ago"
        elif diff.seconds > 60:
            return f"Posted {int(diff.seconds/60)} minutes ago"
        return "Posted just now"

    def get_info(self):
        return {
            "pk" : self.pk,
            "title" : self.title,
            "description" : self.description,
            "date_posted" : self.date_posted,
            "status" : self.is_completed,
            "region" : self.region,
            "job_type" : self.jobtype,
            "war" : str(self.war),
        }

# Acceptance object tying a user to a bounty
class Acceptance(models.Model):

    bounty = models.ForeignKey(Bounty,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_info(self):
        return {
            "pk" : self.pk,
        }

class Completion(models.Model):

    bounty = models.ForeignKey(Bounty,on_delete=models.CASCADE,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    rejection_reason = models.TextField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)

    team = models.ForeignKey(Team,on_delete=models.CASCADE,null=True)

    class Options(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    is_completed = models.CharField(max_length=8,choices=Options.choices,default=Options.PENDING)

    def get_absolute_url(self):
        return reverse("bounty-detail",kwargs={"pk": self.bounty.id})

    def get_info(self):
        return {
            "pk" : self.pk,
            "title" : self.title,
            "description" : self.description,
            "date_posted" : self.date_posted,
            "status" : self.is_completed,
        }

    def get_age(self):
        
        diff = timezone.now() - self.date_posted

        if diff.days > 0:
            return f"Posted {diff.days} days ago "
        elif diff.seconds > 3600:
            return f"Posted {int(diff.seconds / 3600)} hours ago"
        elif diff.seconds > 60:
            return f"Posted {int(diff.seconds/60)} minutes ago"
        return "Posted just now"

class Images(models.Model):

    bounty = models.ForeignKey(Bounty,on_delete=models.CASCADE,null=True)
    completion = models.ForeignKey(Completion,on_delete=models.CASCADE,null=True)
    image = ImageField(upload_to="bounty_images")

    def delete(self,*args,**kwargs):
        storage, path = self.image.storage, self.image.path
        storage.delete(path)

class Message(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.user} {self.text}"

class Channel(models.Model):

    name = models.CharField(max_length=64,null=False,default="None")
    discordid = models.CharField(max_length=32,null=False,default="None")
    types = models.IntegerField(default=0)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

    # Type Byte mappings
    # 1  1000000 LOGI
    # 2  0100000 DEMOLITION
    # 4  0010000 PARTISAN
    # 8  0001000 CONSTRUCTION
    # 16 0000100 COMBAT
    # 32 0000010 REFUEL
    # 64 0000001 OTHER

class BountyNotification(models.Model):

    channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
    text = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.channel.name} {self.text}"