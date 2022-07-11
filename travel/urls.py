from django.contrib import admin
from django.urls import path, include
from travel.place_api import get_category, get_category_api_data, save_place_result, TravelListCountryView, TravelCategoryDetailView, place_detail_delete, place_location_delete, place_category_delete
from travel.views import TravelDestinationView
from . import views

app_name = 'travel'


urlpatterns = [
    path('', views.travelsearch, name='home'),
    path('travel-search/', views.travelsearch, name='travel-search'),
    path('travel-destination/', views.TravelDestinationView.as_view(), name='travel-destination'),
    path('travel-map/', views.MapView.as_view(), name='travel-map'),
    path('travel-weather/', views.weatherView, name='travel-weather'),
    path('travel-currency/', views.currencyView, name='travel-currency'),
    path('travel-get-category/', get_category, name='get-category'),
    path('travel-place-results/<int:final_cat_id>/<str:category>/', views.placeInfoView, name='place-results'),
    path('travel-save-results/', save_place_result, name='save-place-result'),  
    path('travel-country/<str:country>/', TravelListCountryView.as_view(), name='travel-country'),  
    path('travel-category-detail/<str:country>/<str:category>/', TravelCategoryDetailView.as_view(), name='travel-category-detail'),
    path('place-detail-delete/<int:place_id>/', place_detail_delete, name='place-detail-delete'),
    path('place-location-delete/<str:place_location>/', place_location_delete, name='place-location-delete'),
    path('place-category-delete/<str:place_location>/<str:category>/', place_category_delete, name='place-category-delete')
]
