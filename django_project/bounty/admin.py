from django.contrib import admin
from .models import Acceptance, Bounty, Completion, Images, Team, War, Message, Channel, BountyNotification
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.register(Team) # teams does not need export, it is a fixture
admin.site.register(Message) # messages only persist in db for a minute
admin.site.register(BountyNotification) # same for bounty notifs

# BOUNTY
class BountyResource(resources.ModelResource):

    class Meta: 
        model = Bounty

class BountyAdmin(ImportExportModelAdmin):
    resource_class = BountyResource

admin.site.register(Bounty, BountyAdmin)

# COMPLETION
class CompletionResource(resources.ModelResource):

    class Meta: 
        model = Completion

class CompletionAdmin(ImportExportModelAdmin):
    resource_class = CompletionResource

admin.site.register(Completion, CompletionAdmin)

# IMAGES
class ImagesResource(resources.ModelResource):

    class Meta: 
        model = Images

class ImagesAdmin(ImportExportModelAdmin):
    resource_class = ImagesResource

admin.site.register(Images, ImagesAdmin)

# WAR
class WarResource(resources.ModelResource):

    class Meta: 
        model = War

class WarAdmin(ImportExportModelAdmin):
    resource_class = WarResource

admin.site.register(War, WarAdmin)

# ACCEPTANCE
class AcceptanceResource(resources.ModelResource):

    class Meta: 
        model = Acceptance

class AcceptanceAdmin(ImportExportModelAdmin):
    resource_class = AcceptanceResource

admin.site.register(Acceptance, AcceptanceAdmin)

# CHANNEL
class ChannelResource(resources.ModelResource):

    class Meta: 
        model = Channel

class ChannelAdmin(ImportExportModelAdmin):
    resource_class = ChannelResource

admin.site.register(Channel, ChannelAdmin)