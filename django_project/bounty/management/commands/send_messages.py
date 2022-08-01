from django.core.management.base import BaseCommand
from bounty.models import Message
from users.models import Profile
from bounty.models import Message
from bounty.utils import messageAll

class Command(BaseCommand):
    help = "Checks the Foxhole WAR API for a new war. If new war has started, all players are un-verified"

    def add_arguments(self, parser):
        parser.add_argument('message', nargs='+', type=str)

    def handle(self, *args, **options):

        message = options["message"][0]
        messageAll(message)
