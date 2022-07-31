from django.core.management.base import BaseCommand
from bounty.models import Message
from users.models import Profile
from bounty.models import Message

class Command(BaseCommand):
    help = "Checks the Foxhole WAR API for a new war. If new war has started, all players are un-verified"

    def add_arguments(self, parser):
        parser.add_argument('message', nargs='+', type=str)

    def handle(self, *args, **options):

        message = options["message"]
        p = Profile.objects.filter(verified=True,discordmessage=True)

        for profile in p.iterator():

            m = Message(user=profile.user,text=message)
            m.save()
