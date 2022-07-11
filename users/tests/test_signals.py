from django.test import TestCase
from users.models import CustomUser
from django.contrib.auth import get_user_model



class UsersSignalsTest(TestCase):

    
    def test_login_count_increments_signals(self):
        
        # Using a force_login method which details of how a user logged in aren't important, the [0] is selecting the authentication backend in settings
        User = get_user_model()
        logged_in = self.client.force_login(User.objects.get_or_create(username='test@user.com')[0])
        self.assertTrue(CustomUser.login_count, 1)
        