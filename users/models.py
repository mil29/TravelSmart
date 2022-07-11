from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils import timezone



#  Custom user 
class UserManager(BaseUserManager):

    def create_user(self, email, username, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model (email=email, 
                           username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(email, username, password, **other_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    email       = models.EmailField(max_length=100, unique=True)
    username    = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(null=True, unique=True)
    joined_on   = models.DateTimeField(default=timezone.now)
    is_staff    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    login_count = models.PositiveIntegerField(default=0)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'   # changing username requirement to only email login
    REQUIRED_FIELDS = ['username']  # required fields when creating superuser

    def __str__(self):
        return self.email


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super(CustomUser, self).save(*args, **kwargs)



class Profile(models.Model):
    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100)
    age             = models.CharField(max_length=50)
    about           = models.TextField(max_length=250,  blank=True, null=True)
    profile_pic     = models.ImageField(upload_to='profile_pics', default='default_profile_pic/default.jpeg', null=True, blank=True)
    profile_user    = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    updated         = models.DateTimeField(default=timezone.now)
    
    
    
    def __str__(self):
        return self.profile_user.slug



        
    
    


