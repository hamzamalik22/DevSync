from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profiles'),
    path('loginPage/', views.loginUser, name='login-User'),
    path('RegisterPage/', views.RegisterUser, name='Register-User'),
    path('logoutPage/', views.logoutUser, name='logout-User'),
    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
]
