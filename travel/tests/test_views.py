from django.test import TestCase, RequestFactory
from requests import request
from travel.models import RecentSearches
from users.models import CustomUser, Profile
from django.contrib.auth import get_user_model
from travel.views import TravelDestinationView, travelsearch, MapView, weatherView
from travel.forms import SearchForm
from django.contrib.messages import get_messages


class TravelViewsTest(TestCase):
    
    def setUp(self):
        User = get_user_model()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='user@user.com', username='user123', password='password7711')
        profile = Profile.objects.get(profile_user=self.user)
        recent = RecentSearches.objects.create(destination="test_country", search_profile=profile)
        
    
    def test_Travel_Destination_view_context(self):
        request = self.factory.get('travel-destination/')
        request.user = self.user
        
        response = TravelDestinationView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    
    def test_travelsearch_view(self):
        request = self.factory.get('travel-search/')
        request.user = self.user
        form_data = {'destination': 'test_country'}
        form = SearchForm(data=form_data)
        
        response = travelsearch(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.is_valid())
    
    
    def test_MapView_context(self):
        request = self.factory.get('travel-map/')
        request.user = self.user
        
        response = MapView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
        