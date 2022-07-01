from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Bounty, Completion
import logging

# create a profile automatically when a user is created
# Completion saved -> post_save signal -> create profile function -> (sender,instance,created)
@receiver(post_save,sender=Completion)
def create_completion(sender,instance,created,**kwargs):

    if created:
        bounty = instance.bounty
        bounty.num_submissions += 1
        bounty.save()

@receiver(pre_delete,sender=Completion)
def log_deleted_question(sender, instance, using, **kwargs):
    bounty = instance.bounty
    bounty.num_submissions -= 1
    bounty.save()