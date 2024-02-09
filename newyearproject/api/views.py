from rest_framework.decorators import api_view
from app2024.models import Project
from .serializers import ProjectSerializers
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'Name':'Hamza'},
        {'Reg':'22-CS-86'},
        {'Team':'United'},
        {'nickname':'python'},
    ]

    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializers(projects, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def getProject(request,pk):
    projects = Project.objects.get(id = pk)
    serializer = ProjectSerializers(projects, many=False)
    return Response(serializer.data)
    