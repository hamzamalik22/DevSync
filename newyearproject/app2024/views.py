from django.shortcuts import render,redirect
from .models import *
from .forms import *

def homepage(request):
    projects = Project.objects.all()
    context = {'page' : 'Dev Sync','projects' : projects}
    return render(request,'homepage.html',context)

def projectpage(request,pk):
    project = Project.objects.get(id = pk)
    context = {'page' : project.title,'project' : project}
    return render(request,'app2024/project.html',context)

def createProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project')

    context = {'page' : 'Create Project','form' : form}
    return render(request,'app2024/project_form.html',context)  

def updateProject(request, pk):
    project = Project.objects.get(id = pk)
    form = ProjectForm(instance = project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance = project)
        if form.is_valid():
            form.save()
            return redirect('project')

    context = {'page' : 'Update Project','form' : form}
    return render(request,'app2024/project_form.html',context)  

def deleteProject(request, pk):
    project = Project.objects.get(id = pk)
    if request.method =='POST':
        project.delete()
        return redirect('project')

    context = {'page' : 'Create Project','project' : project}
    return render(request,'delete_template.html',context)