from django.contrib import admin
from .models import BountyImage,User,Bounty,Completion

# Register your models here.

admin.site.register(BountyImage)
admin.site.register(User)
admin.site.register(Bounty)
admin.site.register(Completion)
