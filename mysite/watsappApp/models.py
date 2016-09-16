import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", default=None)
    receiver = models.ForeignKey(User, related_name="receiver", default=None)
    text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return str(self.sender) + " sent a message on " + str(self.pub_date.date()) + " at " + str(self.pub_date.time()) + ": " + self.text

