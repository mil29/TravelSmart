from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import CustomUser, Profile
from travel.models import Places
from .forms import UserCreateForm, ProfileAddForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


User = get_user_model()



# Class based Profile detail view
class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile.html'
    
    # def get_object(self, **kwargs):
    #     return Profile.objects.get(profile_user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Profile'] = Profile.objects.get(profile_user=self.request.user)
        context['recent_places'] = Places.objects.filter(place_user=self.request.user).values('location').distinct()
        return context


# Profile view with edit form updateview 
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileAddForm
    template_name = 'users/profile_edit.html'
    
    def get_object(self, **kwargs):
        return Profile.objects.get(profile_user=self.request.user)
        
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Profile Updated Successfully')
        return reverse_lazy('profile', kwargs={'slug': self.request.user.slug, 'pk': self.request.user.id})
    

#  Register Class based View
class RegisterView(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Account Created'


# Custom login redirects users to profile page with slug argument
class MyLoginView(LoginView):
    
    # Count login_count and display message accordingly 
    def get_success_url(self):
        if self.request.user.login_count <= 1:
            # messages.WARNING stays visible 10 secs .SUCCESS alert only 4 secs (customized in custom.js)
            messages.add_message(self.request, messages.WARNING, 'Welcome to the site please add some info to your profile' .format(username=self.request.user.slug))
            return reverse_lazy('profile', kwargs={'slug': self.request.user.slug, 'pk': self.request.user.id})
        else:
            messages.add_message(self.request, messages.SUCCESS, 'Welcome Back {username}'.format(username=self.request.user.slug))
            return reverse_lazy('profile', kwargs={'slug': self.request.user.slug, 'pk': self.request.user.id})
            


# clears the profile image and sets it back to default if user doesn't want to upload a new profile image
def delete_profile_image(request, slug, pk):
    image = Profile.objects.get(profile_user=pk)
    image.profile_pic = 'default_profile_pic/default.jpeg'
    image.save()
    return redirect('profile', slug=slug, pk=pk)
 
