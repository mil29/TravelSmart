from datetime import datetime
from travel.models import RecentSearches
from django.conf import settings
import requests
from datetime import datetime
import pandas as pd
import calendar
from dateutil.parser import parse




#  creating country capitals dict from a csv of all world countries and their capital city names 
df = pd.read_csv("travel/country-capital.csv")

# function gives back the capital name from the travelsearch input entry by checking against the country name in the pandas dataframe
def find_capital_name(country):
    try:
        capital = df.loc[df['country'] == country, 'capital']
        return capital.values[0]
    except:
        return None


# function to workout which svg icon is needed based on weather api description
def get_svg_icon(description):
    if 'rain' in description:
        if 'light' in description:
            icon = 'travel/svg_icons/svg_drizzle.html'
        else:
            icon = 'travel/svg_icons/svg_rain.html'
            
    elif 'cloud' in description:
        if 'broken' or 'scattered' or 'overcast' in description:
            icon = 'travel/svg_icons/svg_overcast.html'
        if 'few' in description:
            icon = 'travel/svg_icons/svg_cloudy.html'   
                
    elif 'clear' in description:
        icon = 'travel/svg_icons/svg_clear_sky.html'
    
    elif 'thunder' or 'lightning' in description:
        icon = 'travel/svg_icons/svg_thunderstorms.html'
    
    elif 'snow' in description:
        icon = 'travel/svg_icons/svg_snow.html'
    
    elif 'sleet' in description:
        icon = 'travel/svg_icons/svg_sleet.html'
    
    elif 'hail' in description:
        icon = 'travel/svg_icons/svg_hail.html'
    
    else:
        icon = 'travel/svg_icons/svg_unavailable.html'
    
    return icon
        


# Below functions are api request functions

#  function to retrieve lat and lng from geocode google api search
def get_lat_lon(user):
    try:
        place = RecentSearches.objects.filter(search_profile=user.profile).order_by('-search_date')[0]
        capital = find_capital_name(str(place))
        if capital:
            place = capital

        response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={settings.GOOGLE_API_KEY}")
        data = response.json()
        # print(data)

        #  get latitude and longitude from geocode api search
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        full_name = data['results'][0]['formatted_address']
        return lat, lng, full_name
    except IndexError:
        return None


#  function to get data from open weather api this function also filters the data into a forecast_7_day dict
def get_weather_data(user):
  
    # calls get_lat_lon function to retrieve coordinates of place from user destination search
    lat, lng, full_name = get_lat_lon(user)
    
    weather_api_key = settings.WEATHER_API_KEY
    params = {
        'lat': lat,
        'lon': lng,
        'exclude': "current,minutely,hourly,alerts",
        'units': 'metric',
        'appid': weather_api_key,
    }
    response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall?", params=params)
    data = response.json()
    # print(data)

    # Creates nested dictinary from api results with day name, description, temp_min and temp_max 
    forecast_7_day = {}
    count = 1
    while count < 6:
        for item in data['daily']:
            if item['dt'] or item['temp'] or item['weather']:
                # this converts the unix timestamp to datetime day name
                day = datetime.fromtimestamp(item['dt']).strftime('%A')
                forecast_7_day[f'day {count}'] = {
                    'day': day, 
                    'description': item['weather'][0]['description'], 
                    'temp_min': item['temp']['min'], 
                    'temp_max':item['temp']['max']
                    }
                count += 1
                
                
    # cutting out only day 1 from foreast_7_day to use for main weather display also adding new svg key 
    today_forecast = {}
    today_forecast['day 1'] = forecast_7_day['day 1']
    new_svg_key = {'svg' : get_svg_icon(today_forecast['day 1']['description'])}
    today_forecast['day 1'].update(new_svg_key)
    # print(today_forecast)
    
    #  removing day 1 and day 8 from 7 day forecat dict to use for 6 weather days in weather widget
    keys_to_remove = ['day 1', 'day 8']
    for key in keys_to_remove:
        del(forecast_7_day[key]) 

    
    # workout from each weather daily description which svg icon will be suitable
    # forecast 7 days icons 
    # adding svg link to forecast_7_day dict getting svg link from get_svg_icon function
    for day in forecast_7_day:
        svg_link = get_svg_icon(forecast_7_day[day]['description'])
        forecast_7_day[day]['svg'] = svg_link
    
    # print(forecast_7_day)
    return full_name, today_forecast, forecast_7_day