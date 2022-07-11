from ctypes import addressof
from django.db import models
from django.forms import CharField
from django.utils import timezone
from users.models import Profile, CustomUser



class RecentSearches(models.Model):
    destination     = models.CharField(max_length=150, blank=False, null=False)
    search_date     = models.DateTimeField(default=timezone.now)
    search_profile  = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=False)
    
    
    def __str__(self):
        return self.destination
    


class Places(models.Model):
    name        = models.CharField(max_length=150, blank=False)
    address     = models.CharField(max_length=150, blank=True)
    website     = models.CharField(max_length=150, blank=True)
    fsq_id      = models.CharField(max_length=100, blank=False)
    category    = models.CharField(max_length=100, blank=False)
    location    = models.CharField(max_length=100, blank=False)
    place_user  = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
