from django.test import TestCase
from travel.models import RecentSearches, Places
from users.models import CustomUser, Profile
from django.contrib.auth import get_user_model




class TravelModelsTest(TestCase):
    
    def test_recentsearches_model_str_return(self):
        User = get_user_model()
        user = User.objects.create_user(email='user@user.com', username='user123', password='password7711')
        profile = Profile.objects.get(profile_user=user)
        recent = RecentSearches.objects.create(destination="test_country", search_profile=profile)
        
        self.assertEqual(str(recent), recent.destination)
    
    
    def test_places_model_str_return(self):
        User = get_user_model()
        user = User.objects.create_user(email='user@user.com', username='user123', password='password7711')
        place = Places.objects.create(name="test_name", fsq_id="12345", category="test_category", location="test_location", place_user=user)
        
        self.assertEqual(str(place), place.name)
    

