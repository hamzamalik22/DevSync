from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profiles'),
    path('loginPage/', views.loginUser, name='login-User'),
    path('RegisterPage/', views.RegisterUser, name='Register-User'),
    path('logoutPage/', views.logoutUser, name='logout-User'),
    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('user-account/', views.userAccount, name='user-account'),
    path('edit-account/', views.editAccount, name='edit-account'),
    path('add-skill/', views.addSkill, name='add-skill'),
    path('edit-skill/<str:pk>/', views.editSkill, name='edit-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),
]
