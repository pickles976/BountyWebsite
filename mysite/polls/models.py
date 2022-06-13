from django.db import models

# Image used for any kind of thing
# TODO: switch to legitimate image usage in django
class Image(models.Model):

    def __str__(self):
        return f"{self.url}"
    
    url = models.CharField(max_length=200)

# User
# TODO: override with Django auth user model
class User(models.Model):

    def __str__(self):
        return f"{self.pk}"

    name = models.CharField(max_length=100)
    password = models.CharField(max_length=32,blank=True,null=True)
    payment_info = models.CharField(max_length=35,blank=True,null=True)
    image = models.ForeignKey(Image,on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now=True)


# A bounty object to be posted by a user
class Bounty(models.Model):

    def __str__(self):
        return f"{self.description}"

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)

    description = models.CharField(max_length=200,default="",blank=True,null=True)
    price = models.DecimalField(max_length=200,default=0,decimal_places=5,max_digits=20)
    num_accepted = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

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
    images = models.ManyToManyField(Image)

    coordinates = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    time_created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING)


