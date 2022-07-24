import django_filters
from bounty.models import Bounty

class BountyFilter(django_filters.FilterSet):

    class Meta:
        model = Bounty
        fields = ["job_type","region"]