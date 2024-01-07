from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def homepage(request):
    # <---- Searching ---->
    q = ''
    if request.GET.get('q'):
        q = request.GET.get('q')

    tags = Tag.objects.filter(name__icontains = q)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=q) | 
        Q(description__icontains=q) | 
        Q(owner__name__icontains=q) |
        Q(tags__in=tags) 
    )

        # <---- Pagination ---->
    page = request.GET.get('page')
    results = 3
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)


    context = {'page' : 'Projects','projects' : projects, 'q' : q, 'paginator' : paginator}
    return render(request,'homepage.html',context)

def projectpage(request,pk):
    project = Project.objects.get(id = pk)
    context = {'page' : project.title,'project' : project}
    return render(request,'app2024/project.html',context)

@login_required(login_url="login-User")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project =  form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('user-account')

    context = {'page' : 'Create Project','form' : form}
    return render(request,'app2024/project_form.html',context)  

@login_required(login_url="login-User")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id = pk)
    form = ProjectForm(instance = project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance = project)
        if form.is_valid():
            form.save()
            return redirect('project')

    context = {'page' : 'Update Project','form' : form}
    return render(request,'app2024/project_form.html',context)  


@login_required(login_url="login-User")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id = pk)
    if request.method =='POST':
        project.delete()
        return redirect('project')

    context = {'page' : 'Create Project','project' : project}
    return render(request,'delete_template.html',context)