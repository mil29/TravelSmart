import os
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import CustomUser, Profile
from django.contrib.auth.signals import user_logged_in

 

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(profile_user=instance)
  
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
        instance.profile.save()


def login_user(sender, request, user, **kwargs):
    user.login_count = user.login_count + 1
    user.save()


user_logged_in.connect(login_user)



#  Delete old profile image of user from database
@receiver(post_delete, sender=Profile)
def profile_image_delete(sender, instance, **kwargs):
    if instance.profie_pic:
        if os.path.isfile(instance.profile_pic):
            os.remove(instance.profile_pic)



# This then updates db with new profile image and deletes old file
@receiver(pre_save, sender=Profile)
def profile_image_update(sender, instance, **kwargs):
    if not instance.pk:
        return False
    
    if sender.objects.get(pk=instance.pk).profile_pic:
        old_image = sender.objects.get(pk=instance.pk).profile_pic
        new_image = instance.profile_pic
        # check old image is not new image then overwrites if old iamge is default image then ignores
        if not old_image == new_image and 'default_profile_pic/default.jpeg' not in old_image:
            if os.path.isfile(old_image):
                os.remove(old_image)
    else:
        return False


        
        
        
        
    