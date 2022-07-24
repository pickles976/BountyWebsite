from django.contrib import admin
from .models import Acceptance, Bounty, Completion, Images, Team, War, Message

admin.site.register(Bounty)
admin.site.register(Completion)
admin.site.register(Images)
admin.site.register(Team)
admin.site.register(War)
admin.site.register(Acceptance)
admin.site.register(Message)

