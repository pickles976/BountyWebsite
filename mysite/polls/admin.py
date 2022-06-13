from django.contrib import admin
from .models import Image,User,Bounty,Completion

# Register your models here.

admin.site.register(Image)
admin.site.register(User)
admin.site.register(Bounty)
admin.site.register(Completion)
