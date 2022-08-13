from django.contrib import admin
from .models import Profile, ProfileImage, DailyVisit

admin.site.register(Profile)
admin.site.register(ProfileImage)
admin.site.register(DailyVisit)