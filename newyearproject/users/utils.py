from django.db.models import Q
from .models import *


def SearchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skills.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(headline__icontains=search_query) | 
        Q(skills__in=search_query)  
    )

    return profiles, search_query