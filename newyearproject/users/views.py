from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required

def profile(request):
    profiles = Profile.objects.all()
    context = {'page' : 'Developers','profiles' : profiles}
    return render(request, 'profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id = pk)
    topSkills = profile.skills_set.exclude(description__exact="")
    otherSkills = profile.skills_set.filter(description="")
    context = {'page' : 'Profile', 'profile': profile,'topSkills': topSkills,'otherSkills': otherSkills}
    return render(request, 'user_profile.html', context)

@login_required(login_url="login-User")
def userAccount(request):
    profile = request.user.profile
    context = {'page' : 'Profile', 'profile': profile}
    return render(request, 'user_account.html',context)

@login_required(login_url="login-User")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-account')

    context = {'page' : 'Edit', 'form': form}
    return render(request, 'profile_form.html',context)

@login_required(login_url="login-User")
def addSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.info(request, 'Skill is added Successfully')
            return redirect('user-account')

    context = {'form' : form}
    return render(request, 'skill_form.html',context)


@login_required(login_url="login-User")
def editSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id = pk)
    form = SkillForm(instance = skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance = skill)
        if form.is_valid():
            form.save()
            messages.info(request, 'Skill updated Successfully')
            return redirect('user-account')

    context = {'page' : 'Edit Skill', 'form': form}
    return render(request, 'skill_form.html',context)

@login_required(login_url="login-User")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id = pk)

    if request.method =='POST':
        skill.delete()
        return redirect('user-account')

    context = {'page' : 'Delete Skill','project' : skill}
    return render(request,'delete_template.html',context)

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