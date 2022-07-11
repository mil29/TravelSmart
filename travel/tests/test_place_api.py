from django.test import TestCase
from requests import request
from travel.place_api import *
import numpy as np



class PlaceApiViewsTest(TestCase):
    
    
    def test_top_level_cat_id_output(self):
        result = top_level_cat_id('Restaurant')
        self.assertIsInstance(result, int)
    
    
    def test_get_category_options_output(self):
        result = get_category_options('Restaurant')
        result2 = get_category_options('Cafe')
        self.assertIsInstance(result, np.ndarray)
        self.assertIsInstance(result2, int)
        
