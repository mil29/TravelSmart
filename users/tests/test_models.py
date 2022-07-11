from django.test import TestCase
from users.models import CustomUser, Profile
from django.contrib.auth import get_user_model


class UsersManagersTest(TestCase):
    
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='user@user.com', username='user123', password='password7711')
        
        self.assertEqual(user.email, 'user@user.com')
        self.assertEqual(user.username, 'user123')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(TypeError):
            User.objects.create_user(username='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', username='user123', password='password7711')
        
        # Checks return str value should be equal to user email 
        self.assertEqual(str(user), 'user@user.com')
        
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', username='superuser123', password='password7711')
        
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.username, 'superuser123')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='super@user.com', username='superuser123', password='password7711', is_superuser=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='super@user.com', username='superuser123', password='password7711', is_staff=False)
        
        
        
    
class ProfileTest(TestCase):
    
    def test_profile(self):
        User = get_user_model()
        user = User.objects.create_user(email='user@user.com', username='user123', password='password7711')
        profile = Profile.objects.get(profile_user=user)
        
        # Checks whether profile is created automatically through signals after a user is created 
        self.assertEqual(user.profile, profile)
        #  checks the return str of profile should be slug: (users username)
        self.assertEqual(str(profile), 'user123')
    

        

        
