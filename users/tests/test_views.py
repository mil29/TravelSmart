from django.test import TestCase, RequestFactory
from users.models import Profile, CustomUser
from django.contrib.auth import get_user_model
from users.views import *
from django.urls import reverse
from travel.models import Places


User = get_user_model()


class ProfileViewTest(TestCase):
    
    def setUp(self):
        User = get_user_model()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='user@user.com', username='user123', password='password7711')
        self.profile = Profile.objects.get(profile_user=self.user)
        place = Places.objects.create(name="test_name", fsq_id="12345", category="test_category", location="test_location", place_user=self.user)

        
    def test_profileview_get_context(self):
        
        request = self.factory.get('profile/')
        request.user = self.user
        
        response = ProfileView.as_view()(request, **{'slug':self.user.slug, 'pk':self.user.id})
        self.assertEqual(response.status_code, 200)
        

   
    
        
