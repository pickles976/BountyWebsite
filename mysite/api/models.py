from django.db import models
import string
import random
from uuid import uuid4

# def generate_unique_code():
#     length = 6
    
#     while True:
#         code = "".join(random.choices(string.ascii_uppercase,k=length))
#         if Room.objects.filter(code=code).count() == 0:
#             break
    
#     return code

class Image(models.Model):
    unique_id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    image = models.ImageField(upload_to="images")

# Create your models here.
class User(models.Model):

    def __str__(self):
        return f"{self.name},{self.unique_id}"
    
    unique_id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32,null=True,blank=True)
    payment_info = models.CharField(max_length=32,null=True,blank=True)
    # bounties_completed
    time_created = models.DateTimeField(auto_now_add=True)

class Bounty(models.Model):

    def __str__(self):
        return f"{self.description},{self.unique_id}"

    unique_id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=64,blank=False,null=False)
    images = models.ManyToManyField(Image)
    price = models.DecimalField(max_digits=10,decimal_places=5)
    num_accepted = models.IntegerField(default=0,null=False,blank=True)
    is_completed = models.BooleanField(default=False,null=False,blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

class Completion(models.Model):

    STATUS_CHOICES = (
        ("PENDING","Pending"),
        ("ACCEPTED","Accepted"),
        ("REJECTED","Rejected")
    )
    
    unique_id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    parent_bounty = models.ForeignKey(Bounty,on_delete=models.CASCADE)
    coordinates = models.CharField(max_length=100)
    images = models.ManyToManyField(Image)
    description = models.CharField(max_length=512)
    status = models.CharField(max_length=16,choices=STATUS_CHOICES,default="PENDING",blank=True,null=False)
    time_created = models.DateTimeField(auto_now_add=True)


