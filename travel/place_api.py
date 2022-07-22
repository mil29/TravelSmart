from unicodedata import category
from numpy import place
import requests
from django.conf import settings
from travel.weather_api import get_lat_lon
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.shortcuts import render, redirect
from django.contrib import messages
import time
from .models import Places, RecentSearches, Profile
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



# load categories csv into pandas dataframe
# pd.set_option('display.max_rows', None)
df = pd.read_csv('travel/foursquare_categories.csv', index_col=False, sep='\s*[,>]\s*', engine='python', names=['id', 'main_category', 'sub1_category', 'sub2_category', 'sub3_category'])



@login_required
def get_category(request):
    

    main = main_category_options()
    
    #  adds some popular category buttons at top of category search page
    popular = ['Restaurant', 'Hotel', 'Shopping Mall', 'Cafe', 'Museum']
    
    if request.method == 'POST' and "category_data" in request.POST:
        
        try:
        
            category = request.POST.get('category_data', None)
            
            
            response_data = {}
            
            category_options = get_category_options(category)
            
            #  calls top_level_id function to recieve a cat id of main cat even if it has sub categories, like movie theater has 2 sub categories but this gets just the 'movie theater' cat id
            top_cat_id = top_level_cat_id(category)

                
            # get column name and column index so elements can be deleted through js when neccessary 
            col_name = df.columns[df.isin([category]).any()][0]
            col_index = df.columns.get_loc(col_name)
            
            
            if type(category_options) == int:
                response_data['id'] = category_options
                response_data['column_number'] = col_index
                response_data['category'] = category
                
            else:
                keys = range(len(category_options))
                response_data['result'] = dict(zip(keys, category_options))
                response_data['column_number'] = col_index
                response_data['top_cat_id'] = top_cat_id
                response_data['category'] = category
            
        
            
            return HttpResponse(
            json.dumps(response_data),
            content_type = "application/json"
                )
            
            
        except IndexError:
            return HttpResponse(
                json.dumps({"Error":"problem getting data"}),
                content_type = "application/json"
            )
     
    # if post request is from submit buton form then send id to get_category_id function for API data request
    elif request.method == 'POST' and "get_cat_id" in request.POST:
        
        # request id from submit button value  
        final_cat_id = request.POST.get('get_cat_id').split('-')
        
        # send final_cat_id to get_category_id function to request data from API
        # try except to catch indexerror if api returns nothing
        try:
            return redirect('travel:place-results', final_cat_id=final_cat_id[0], category=final_cat_id[1])
        except IndexError:
            messages.add_message(request, messages.ERROR, "Sorry no data for that category, try another")
            return redirect('travel:get-category')
            
    context = {
        "main_categories": main,
        "popular_categories": popular
    }
    
    return render(request, 'travel/travel-get-category.html', context=context)

    

def main_category_options():
    
    main_categories = df['main_category'].unique()
    return main_categories


def top_level_cat_id(category):
    
    cat_column = df.columns[df.isin([category]).any()][0]
    ci = df.columns.get_loc(cat_column)
    
    if ci == 2:
        # gets the top level category item id after main_category options even if it has sub categories after
        this_id = df.loc[df['sub1_category'] == category, 'id'].head(1)
        if len(this_id) > 0:
            top_cat_id = this_id.item()
            return top_cat_id
    if ci == 3:
        this_id = df.loc[df['sub2_category'] == category, 'id'].head(1)
        if len(this_id) > 0:
            top_cat_id = this_id.item()
            return top_cat_id


def get_category_options(category):
    
    # print(category)
    # gets column name of value from pd dataframe
    cat_column = df.columns[df.isin([category]).any()][0]
    # print(cat_column)
    # finds the index of the column that has category as value
    ci = df.columns.get_loc(cat_column)
    # string literal for selecting next category
    next_category = f'sub{ci}_category'
    # print(next_category)
    # df query to find all possible options of category value from next column
    sub_categories = df.loc[df[cat_column] == category, next_category].dropna().unique()
    # print(sub_categories)
    
    if len(sub_categories) < 1:
        get_id = df[df.values == category]['id'].values.item()
        return get_id
    else:
        return sub_categories



#  fucntions that searches foursquare api using the final category id from user selection, to get results data
@login_required
def get_category_api_data(request, final_id, category):

    #  get data reponse from foursquare api usng category_id

    user = request.user
    lat, lon, full_name = get_lat_lon(user)
    # print(lat,lon)
    
    lat_lon = f"{lat},{lon}"
    # print(lat_lon)
    
    headers = {
    "Accept": "application/json",
    "Authorization": settings.FOURSQUARE_API_KEY
    }
    
    params = {
        'll' : lat_lon,
        'radius': 20000,
        'categories': final_id,
        'fields': 'fsq_id,name,location,description,website,rating,price,photos',
        'limit': 50,
        # 'min_price': 4, # set price 1 to 4 (1 most affordable , 4 most expensive)
        # 'max_price': 4, # same as min price between 1 - 4 for price of venue
    }
    
    url = "https://api.foursquare.com/v3/places/search?"

    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    # print(data)
    #  filter reponse data
    place_data = {}
    
    count = 1
    for info in data['results']:
        try:
            place_data[f'place{count}'] = {
                'fsq_id': info['fsq_id'],
                'name': info['name'],
                'address': info['location']['formatted_address'],
                'url': info['website'],
                'images': info['photos'],
                'category': category,
                'rating': info['rating'],
                'description': info['description']
            }
        except KeyError:
            place_data[f'place{count}'] = {
                'fsq_id': info['fsq_id'],
                'name': info['name'],
                'address': info['location']['formatted_address'],
                'images': info['photos'],
                'category': category,
            }
            
        count += 1
    
    # print(place_data)

    return place_data

    
@login_required
def save_place_result(request):
    
    if request.method == "POST":
        
        result_dict = {}
        result = request.POST.get('placeSave', None)
        # print(result)
        # splits results from save button to get name, address, url, fsq_id
        search_items = [item for item in result.split('--')]
        # print(search_items)
        
        # loop over range length of search_items list and populate result_dict
        keys = range(len(search_items))
        for i in keys:
            result_dict[i] = search_items[i]
  
        # print(result_dict)
        
        #  get user and profile object to obtain last search of RecentSearches model 
        user = request.user
        profile = Profile.objects.get(profile_user=user)
        location = RecentSearches.objects.filter(search_profile=profile).last()
        
        check_for_duplicate_entry = Places.objects.filter(place_user=user, name=result_dict[0], address=result_dict[1])
        if not check_for_duplicate_entry:
            # create instance of model to add data from places api search if not already in db
            place = Places()
            place.name = result_dict[0]
            place.address = result_dict[1]
            place.website = result_dict[2]
            place.fsq_id = result_dict[3]
            place.category = result_dict[4]
            place.location = location
            place.place_user = user
            place.save()
        

            return HttpResponse(
                json.dumps({'result': 'saved'}),
                content_type = "application/json"
                    )

        else:
            return HttpResponse(
                json.dumps({'result': 'already_saved'}),
                content_type = "application/json"
                    )
            
        
    
    return HttpResponse('Place result has been saved')


#  Lists the users categories for the specific country 
class TravelListCountryView(LoginRequiredMixin, ListView):
    
    model = Places
    template_name = 'travel/travel-country.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['country'] = self.kwargs['country']
        context['country_categories'] = Places.objects.filter(place_user=self.request.user, location=self.kwargs['country']).values('category').distinct()
        return context


#  shows the information the category filtering by country
class TravelCategoryDetailView(LoginRequiredMixin, ListView):
    
    model = Places
    template_name = 'travel/travel-category-detail.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['category_detail'] = Places.objects.filter(place_user=self.request.user, location=self.kwargs['country'], category=self.kwargs['category']).values('id','name', 'address', 'website', 'location', 'category').distinct()
        return context
        

def place_detail_delete(request, place_id):
    place = Places.objects.get(id=place_id)
    place.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def place_location_delete(request, place_location):
    place_location = Places.objects.filter(place_user=request.user, location=place_location)
    place_location.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def place_category_delete(request, place_location, category):
    place_category = Places.objects.filter(place_user=request.user, location=place_location, category=category)
    place_category.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



# old version of creating foursquare_categories dict from csv reader with get_id function below
# #  creating categories dict from foursquare_categories.csv file 
# foursquare_categories = {}
# with open('travel/foursquare_categories.csv', 'r') as file:
#     for rows in csv.reader(file):
#         rows1 = rows[1].split('>')
#         rows1 = [item.strip() for item in rows1]
#         #  populate foursquare_categories dict 
#         foursquare_categories[rows[0]] = rows1

# # print(foursquare_categories)
        

# #  finds the id of category from foursquare categories dict
# def get_foursquare_cat_id(selection):
#     for key, value in foursquare_categories.items():
#         for item in value:
#             if item == selection and (value.index(item) == len(value)-1):
#                 return key
        

# print(get_foursquare_cat_id('International Airport'))