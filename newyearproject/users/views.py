from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm

def profile(request):
    profiles = Profile.objects.all()
    context = {'page' : 'Developers','profiles' : profiles}
    return render(request, 'profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id = pk)
    context = {'page' : 'Profile', 'profile': profile}
    return render(request, 'user_profile.html', context)

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User not found')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or Password Incorrect')

    context = {'page' : 'Login'}
    return render(request,'login_register.html', context)


def RegisterUser(request):
    form = CustomUserCreationForm

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account Created Successfully')
            return redirect('login-User')
        else:
            messages.error(request, 'an error occured during registration')
            
    context = {'page' : 'Register','form' : form}
    return render(request,'login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('profiles')