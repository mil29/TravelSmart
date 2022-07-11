from django.contrib import admin
from django.urls import path, include

from users.signals import profile_image_delete
from . import views


urlpatterns = [
    # path('', views.HomeView.as_view(), name='home'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('profile/<slug:slug>/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile-edit/<slug:slug>/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile-image-remove/<slug:slug>/<int:pk>/', views.delete_profile_image, name='delete_profile_image')
]
