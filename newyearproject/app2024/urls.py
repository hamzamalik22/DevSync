from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('projects/',views.homepage,name='project'),
    path('project/<str:pk>/',views.projectpage,name='projectpage'),
    path('create-project/',views.createProject,name='create-project'),
    path('update-project/<str:pk>',views.updateProject,name='update-project'),
    path('delete-project/<str:pk>',views.deleteProject,name='delete-project'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
