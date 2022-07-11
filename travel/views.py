from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from numpy import NAN
from travel.models import RecentSearches
from travel.forms import SearchForm
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from users.models import Profile
import requests
import pprint
from travel.weather_api import get_weather_data
from travel.place_api import get_category_api_data
from travel.currencies import monetary_symbols
import json
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



pp = pprint.PrettyPrinter(indent=4)


class TravelDestinationView(LoginRequiredMixin, TemplateView):
    template_name: str = 'travel/travel_destination.html'
    
    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            profile = Profile.objects.get(profile_user=self.request.user)
            last_search = RecentSearches.objects.filter(search_profile=profile).order_by('-search_date').values_list('destination', flat=True)[0]
            context['last_search'] = last_search
            return context
        except:
            last_search = "Go to 'Search' and add destination"
            context['last_search'] = last_search
            return context

# this will search via google api for the location and then put the city or country into the api search for the below views
@login_required
def travelsearch(request):
    
    profile = Profile.objects.get(profile_user=request.user)
    recent_destinations = RecentSearches.objects.filter(search_profile=profile).order_by('-search_date').values_list('destination', flat=True).distinct()[:10]
    recent_searches = [item for item in recent_destinations]
    remove_search_duplicates = sorted(set(recent_searches), key=recent_searches.index)
    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.search_profile = profile
            data.destination = form.cleaned_data['destination'].title()
            data.save()
            return redirect('travel:travel-map')
    else:
        form = SearchForm()
    return render(request, 'travel/travel_search.html', {'form': form, 'google_api_key': settings.GOOGLE_API_KEY, 'recent_searches': remove_search_duplicates })
        


#  Map View (will show google map with radiu of 25 miles)

class MapView(LoginRequiredMixin, TemplateView):
    
    template_name = 'travel/map.html'

    def get_context_data(self, **kwargs):
        try:
            profile = Profile.objects.get(profile_user=self.request.user)
            context = super().get_context_data(**kwargs)
            context["google_key"]   = settings.GOOGLE_API_KEY
            context['query']        = 'landmarks'
            context['location']     = RecentSearches.objects.filter(search_profile=profile).order_by('-search_date')[0]
            context['location_title'] = str(context['location']).split(',')[0]
            return context
        except:
            context['nothing'] = "No Destination Selected, Go to search"
            return context
            

      

#  Weather View ( will show forecast for 7 days)
@login_required
def weatherView(request):
 
    try:
        full_name, today_forecast, forecast_7_day = get_weather_data(request.user)
              
        context = {
            'location': full_name,
            'today_forecast': today_forecast,
            'forecast_7_day': forecast_7_day,
        }

        return render(request, 'travel/travel_weather.html', context=context)
    
    except:
        messages.add_message(request, messages.ERROR, "Error locating weather data, add destination")
        return redirect('travel:travel-search')
    


#  Currency View (converter from home currency to destination currency ability to switch)
@login_required
def currencyView(request):
    
    if request.method == 'POST':
        
        try:
            # request data from ajax call 
            amount = float(request.POST.get('amount'))
            currency1 = request.POST.get('curr1', None)
            currency2 = request.POST.get('curr2', None)
            
            if amount and currency1 and currency2:

                #  call exchangerate.host free api to convert currency and return json
                params = {
                    'from'      : currency1,
                    'to'        : currency2,
                    'amount'    : amount
                }
                    
                url = "https://api.exchangerate.host/convert"
                reponse = requests.get(url ,params=params)
                data = reponse.json()
                # print(data)
                
    
                response_data = {}
                
                response_data['from'] = currency1
                response_data['to'] = currency2
                response_data['amount'] = data['query']['amount']
                response_data['result'] = round(data['result'],2)
                response_data['rate'] = data['info']['rate']
                
                
                return HttpResponse(
                    json.dumps(response_data),
                    content_type = "application/json"
                )

        except:
            return HttpResponse(
            json.dumps({"error": "problem with conversion"}),
            content_type="application/json"
            )
            

    context = {
        'monetary_symbols' : monetary_symbols,
    }
    
 
    return render(request, 'travel/travel-currency.html', context=context)



#  Restaurants View (shows top 10 places to eat)
@login_required
def placeInfoView(request, final_cat_id, category):    
    
    try:
        place_data = get_category_api_data(request,final_cat_id, category)
        pd = place_data
        # print(f"this is from placeinfoview {pd}")
    
        context = {
            'place_data': pd,
            'category': category
        }
        
        return render(request, 'travel/travel-place-results.html', context=context)
    
    except:
        messages.add_message(request, messages.ERROR, "Go to search and select a destination")
        return redirect('travel:get-category')




