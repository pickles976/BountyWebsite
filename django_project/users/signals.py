from email.mime import image
from pdb import post_mortem
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# create a profile automatically when a user is created
# User saved -> post_save signal -> create profile function -> (sender,instance,created)
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()

@receiver(post_delete,sender=Profile)
def delete_user(sender,instance,**kwargs):
    instance.user.delete()