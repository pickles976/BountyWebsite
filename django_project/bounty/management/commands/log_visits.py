from django.core.management.base import BaseCommand
from users.models import DailyVisit
from user_visit.models import UserVisit
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Consolidates all UserVisit objects into a dailyvisit object"

    def handle(self, *args, **options):

        age = timedelta(days=3)

        visits = UserVisit.objects.filter(created_at__lte=timezone.now()-age)

        visitsDict = {}

        for visit in visits.iterator():

                date = visit.created_at.date()
                
                if date in visitsDict:
                    visitsDict[date] += 1
                else:
                    visitsDict[date] = 1

        # visits.delete()

        print(visitsDict)

        for date in visitsDict:

            try:
                d = DailyVisit.objects.get(date=date)
                d.numVisits += visitsDict[date]
                d.save()
            except:
                v = DailyVisit(date=date,numVisits=visitsDict[date])
                v.save()

