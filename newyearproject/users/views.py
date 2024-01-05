from django.shortcuts import render
from .models import *

def profile(request):
    profiles = Profile.objects.all()
    context = {'page' : 'Developers','profiles' : profiles}
    return render(request, 'profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id = pk)
    context = {'page' : 'Profile', 'profile': profile}
    return render(request, 'user_profile.html', context)