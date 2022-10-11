from django.contrib import admin
from .models import Profile, ProfileImage, DailyVisit
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Profile
class ProfileResource(resources.ModelResource):

    class Meta: 
        model = Profile

class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource

admin.site.register(Profile, ProfileAdmin)

# Profile Image
class ProfileImageResource(resources.ModelResource):

    class Meta: 
        model = ProfileImage

class ProfileImageAdmin(ImportExportModelAdmin):
    resource_class = ProfileImageResource

admin.site.register(ProfileImage, ProfileImageAdmin)

# Daily Visit
class DailyVisitResource(resources.ModelResource):

    class Meta: 
        model = DailyVisit

class DailyVisitAdmin(ImportExportModelAdmin):
    resource_class = DailyVisitResource

admin.site.register(DailyVisit, DailyVisitAdmin)