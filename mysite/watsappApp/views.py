from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import UserProfile, Message
from django.utils import timezone

def HomeView(request):
    # Checking if the user is authenticated
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('watsappApp:login'))
    else:
        # Getting all the users except the logged in user
        users = UserProfile.objects.filter(~Q(user=request.user))
        context = {'users': users}
        return render(request, 'watsappApp/home.html', context)


def MessageView(request, user_id):
    # Getting the chosen user to chat with
    chosenUser = get_object_or_404(User, pk=user_id)

    # Checking if we are in case that the online user sent a message
    if request.method == "POST":
        # Creating a message object and save it
        message_text = request.POST['message_text']
        if message_text != "":
            message = Message(sender=request.user, receiver=chosenUser, text=message_text, pub_date=timezone.now())
            message.save()

    # Display the message form.
    messages = Message.objects.filter(Q(sender = request.user, receiver = chosenUser) |
                                      Q(receiver = request.user, sender = chosenUser)).order_by('pub_date')
    context = {'messages': messages, "user_id": user_id}
    return render(request, 'watsappApp/message.html', context)

def Login(request):
    context = {'Error': None}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('watsappApp:home'))
        else:
            context['Error'] = "Username or password in not correct"
    return render(request, 'watsappApp/login.html', context)


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('watsappApp:login'))

def Register(request):
    context = {}
    if request.method == "POST":
        # Getting the data the user filled
        user_name = request.POST['username']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']

        # Checking all fields are filled
        if (user_name != "" and password != "" and password_repeat != ""):
            # Checking the passwords are the same
            if (password == password_repeat):
                try:
                    # Checking if the user name already exists
                    user = User.objects.get(username=user_name)
                    context['Error'] = "User name already exists"
                except User.DoesNotExist:
                    # Creating the user
                    new_user = User.objects.create_user(user_name, "", password)
                    new_user_profile = UserProfile(user=new_user)
                    new_user_profile.save()
                    return HttpResponseRedirect(reverse('watsappApp:login'))
            else:
                context['Error'] = "Passwords are not the same"
        else:
            context['Error'] = "Please fill all the fields"

    return render(request, 'watsappApp/register.html', context)
