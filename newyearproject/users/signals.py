from .models import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = "Welcome to DEVSYNC, {0}!".format(profile.name)

        message = (
            f"Hi {profile.name},\n\n"
            "Welcome to DEVSYNC!\n\n"
            "We're excited to have you join our community of talented developers. "
            "At DEVSYNC, you have the opportunity to showcase your skills, share your projects, and connect with other professionals in the industry.\n\n"
            "Here are some tips to get started:\n"
            "1. Complete your profile to let others know who you are and what you do.\n"
            "2. Start uploading your best projects to your portfolio and let your work speak for itself.\n"
            "3. Connect with other developers, explore their profiles, and gain inspiration from their projects.\n\n"
            "Remember, your DEVSYNC portfolio is your digital footprint in the developer community—make it count!\n\n"
            "If you need any assistance or have any questions, our support team is here to help. Feel free to reach out at any time.\n\n"
            "Thank you for choosing DEVSYNC to showcase your talents. We look forward to seeing your amazing work!\n\n"
            "Best regards,\n"
            "The DEVSYNC Team"
        )

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


post_save.connect(createProfile, sender=User)


def userDeleted(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_delete.connect(userDeleted, sender=Profile)


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


post_save.connect(updateUser, sender=Profile)
