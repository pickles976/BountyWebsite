from django.db import models

# User
# TODO: override with Django auth user model
class User(models.Model):

    def __str__(self):
        return f"{self.pk}"

    name = models.CharField(max_length=100)
    password = models.CharField(max_length=32,blank=True,null=True)
    payment_info = models.CharField(max_length=35,blank=True,null=True)
    time_created = models.DateTimeField(auto_now=True)


# A bounty object to be posted by a user
class Bounty(models.Model):

    def __str__(self):
        return f"{self.description}"

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=200,default="",blank=True)
    price = models.DecimalField(default=0,decimal_places=10,max_digits=20,blank=True)
    num_accepted = models.IntegerField(default=0,blank=True)
    time_created = models.DateTimeField(auto_now=True,blank=True)
    is_completed = models.BooleanField(default=False,blank=True)

# Image used for any kind of thing
class BountyImage(models.Model):

    def __str__(self):
        return f"{self.bounty}"
    
    bounty = models.ForeignKey(Bounty,default=None,on_delete=models.CASCADE,blank=True)
    image = models.ImageField(verbose_name="BountyImage")

# A completion of a Bounty
class Completion(models.Model):

    def __str__(self):
        return f"{self.user},{self.bounty}"

    class Status(models.TextChoices):
        ACCEPTED = "accepted"
        REJECTED = "rejected"
        PENDING = "pending"

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bounty = models.ForeignKey(Bounty,on_delete=models.CASCADE)

    coordinates = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    time_created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING)


