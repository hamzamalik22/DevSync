from django.urls import path
from . import views

urlpatterns = [
    path('projects/',views.homepage,name='project'),
    path('project/<str:pk>/',views.projectpage,name='projectpage'),
    path('create-project/',views.createProject,name='create-project'),
    path('update-project/<str:pk>',views.updateProject,name='update-project'),
    path('delete-project/<str:pk>',views.deleteProject,name='delete-project'),
]

