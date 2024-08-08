from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def profile(request):
    # <---- Searching ---->
    q = ""

    if request.GET.get("q"):
        q = request.GET.get("q")

    skills = Skills.objects.filter(name__icontains=q)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=q) | Q(headline__icontains=q) | Q(skills__in=skills)
    )
    # <---- Pagination ---->
    page = request.GET.get("page")
    results = 6
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    context = {"page": "DevSync", "profiles": profiles, "q": q, "paginator": paginator}
    return render(request, "profiles.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skills_set.exclude(description__exact="")
    otherSkills = profile.skills_set.filter(description="")
    context = {
        "page": f"{profile.name}",
        "profile": profile,
        "topSkills": topSkills,
        "otherSkills": otherSkills,
    }
    return render(request, "user_profile.html", context)


@login_required(login_url="login-User")
def userAccount(request):
    profile = request.user.profile
    context = {"page": f"{profile.name}", "profile": profile}
    return render(request, "user_account.html", context)


@login_required(login_url="login-User")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        # print(request.FILES)  # Print the files being uploaded
        # print(request.POST)  # Print the files being uploaded
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user-account")
        else:
            print(form.errors)  # Print form errors to the console

    context = {"page": "Edit Profile", "form": form}
    return render(request, "profile_form.html", context)


@login_required(login_url="login-User")
def addSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.info(request, "Skill is added Successfully")
            return redirect("user-account")

    context = {"page": "Add Skill", "form": form}
    return render(request, "skill_form.html", context)


@login_required(login_url="login-User")
def editSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.info(request, "Skill updated Successfully")
            return redirect("user-account")

    context = {"page": "Edit Skill", "form": form}
    return render(request, "skill_form.html", context)


@login_required(login_url="login-User")
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        return redirect("user-account")

    context = {"page": "Delete Skill", "project": skill}
    return render(request, "delete_template.html", context)


def loginUser(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password1"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User not found")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username or Password Incorrect")

    context = {"page": "Login"}
    return render(request, "login_register.html", context)


def RegisterUser(request):
    form = CustomUserCreationForm

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account Created Successfully")
            return redirect("login-User")
        else:
            messages.error(request, "an error occured during registration")

    context = {"page": "Register", "form": form}
    return render(request, "login_register.html", context)


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect("profiles")


def inbox(request):

    if request.user.is_authenticated == False:
        messages.success(request, "Login to Acces the Inbox Page")
        return redirect("login-User")

    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {
        "page": "Inbox",
        "messageRequests": messageRequests,
        "unreadCount": unreadCount,
        "profile": profile,
    }
    return render(request, "inbox.html", context)


def theMessage(request, pk):
    profile = request.user.profile
    messageRequests = profile.messages.get(id=pk)

    if messageRequests.is_read == False:
        messageRequests.is_read = True
        messageRequests.save()

    context = {"page": "Message", "messageRequests": messageRequests}
    return render(request, "message.html", context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Message sent...")
            return redirect("user-profile", pk=recipient.id)

    context = {"page": "Communicate with Dev", "form": form, "recipient": recipient}
    return render(request, "message_form.html", context)
