from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import UserProfile, Message

# Create your views here.
def HomeView(request):
    users = UserProfile.objects.filter(~Q(user = request.user))
    context = {'users': users}
    return render(request, 'watsappApp/home.html', context)


def MessageView(request, user_id):
    chosenUser = User.objects.get(pk=user_id)
    messages = Message.objects.filter(Q(sender = request.user, receiver = chosenUser) |
                                      Q(receiver = request.user, sender = chosenUser)).order_by('pub_date')
    context = {'messages': messages}
    return render(request, 'watsappApp/message.html', context)