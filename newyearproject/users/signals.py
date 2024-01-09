from .models import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )

        subject = 'Welcome to DEVSYNC'
        welcome = 'Thanks for Joining Devsync....'


        send_mail(
                    subject,
                    welcome,
                    settings.EMAIL_HOST_USER,
                    [profile.email],
                    fail_silently=False,
        )


post_save.connect(createProfile, sender = User)

def userDeleted(sender, instance, **kwargs):
    user = instance.user 
    user.delete()

post_delete.connect(userDeleted, sender = Profile)

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

post_save.connect(updateUser, sender = Profile)