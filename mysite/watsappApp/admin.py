from django.contrib import admin
from .models import Message
from .models import UserProfile

admin.site.register(Message)
admin.site.register(UserProfile)

