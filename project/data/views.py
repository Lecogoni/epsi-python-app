from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import RequestContext
from django.utils import timezone
from datetime import datetime
from datetime import timezone
from .models import Region
from .models import Weather
from django.utils.dateparse import parse_datetime
from django.utils.dateparse import parse_date

def welcome(request):
    import requests
    mydata = {
        'hello': 'Mr Artz', 
     }
    return render(request, 'welcome.html', context=mydata)


def currency(request):
    import requests
    mydata = {
        'msg': '', 
     }
    return render(request, 'bitcoin/bitcoin.html', context=mydata)


# Create your views here.

# home function render home.htm view in template
# load all french regions
# https://geo.api.gouv.fr/decoupage-administratif/regions
# https://geo.api.gouv.fr/regions?nom=Hauts-de-France&limit=5
# https://api.gouv.fr/documentation/api-geo 
def home(request):
    import requests
    import json
    csrfContext = RequestContext(request)

    departments = 'Error'
    regionNumb = 0
    departmentNumb = 0
    regionInfo = []

    if request.method == 'POST':
        coderegion = request.POST['coderegion']
        print(coderegion)
        if len(coderegion) == 1:
            coderegion = '0'+coderegion
        departments_request = requests.get("https://geo.api.gouv.fr/regions/"+str(coderegion)+"/departements?fields=nom,code")
        try:
            departments = json.loads(departments_request.content)
            departmentNumb = len(departments)
        except Exception as e:
            departments = 'Error'

        for department in departments:
            result = load_department_data(department['nom'], department['code'])
            regionInfo.append(result)

    regionData = Region.objects.all().values()
    regionNumb = len(regionData)

    mydata = {
        'regions': regionData, 
        'departements': departments, 
        'regionNumb': regionNumb,
        'departmentNumb' : departmentNumb,
        'regionData' : regionData,
        'regionInfo' :  json.dumps(regionInfo)
     }
    
    return render(request, 'home.html', context=mydata)

# Load departements data
# sum up population of each city in the department / sum the number of cities in the departments
def load_department_data(departmentNom, departmentCode):
    import requests
    import json
    population= 0
    cityNumb = 0
    
    city_request = requests.get("https://geo.api.gouv.fr/departements/"+str(departmentCode)+"/communes?fields=population&format=json&geometry=centre")

    try:
        cites = json.loads(city_request.content)
    except Exception as e:
        departments = 'Error'
    for city in cites:
        population += city['population']
        cityNumb += 1

    result =  {
        "x": departmentNom,
        # 'code': departmentCode,
        "y": population,
        # 'cityNumb': cityNumb,
    }
    # print(result)
    return result


def meteo(request):
    import requests
    import json
    csrfContext = RequestContext(request)

    city = 'Error'
    codeCommune = ''
    nomCommune = ''
    weather = ''
    loaded = None
    cityWeather = []
    cityWeatherData = ['', '', '']

    if request.method == 'POST':
        postcode = request.POST['postcode']
        city_request = requests.get("https://apicarto.ign.fr/api/codes-postaux/communes/"+str(postcode))
        try:
            city = json.loads(city_request.content)
        except Exception as e:
            city = 'Error'


        if city == 'Error':
            city = 'Error'
            loaded = False

        elif 'code' in city:
            city = 'Error'
            loaded = False

        else:
            if len(city) > 1:
                city = city
            if len(city) == 1:
                codeCommune = city[0]['codeCommune']
                nomCommune = city[0]['nomCommune']

                weather_request = requests.get("https://api.meteo-concept.com/api/forecast/daily/1?insee="+str(codeCommune)+"&world=false&start=0&end=1&token=2e1a2c9abced0ba7d8c0378650c7e29f9276069fa502ef9ae0c9e060223c2c86")
            
                try:
                    weather = json.loads(weather_request.content)
                    cityWeatherData = load_weather(codeCommune, weather)
                    loaded = True
                except Exception as e:
                    loaded = False
                    weather = 'Error'

    mydata = {
        'city': city,
        'codeCommune': codeCommune, 
        'nomCommune': nomCommune, 
        'weather': weather,
        'loaded': loaded,
        'cityWeather': json.dumps(cityWeatherData),
        'cityWeatherDate': json.dumps(cityWeatherData[0]),
        'cityWeatherTmin': json.dumps(cityWeatherData[1]),
        'cityWeatherTmax': json.dumps(cityWeatherData[2])
     }

    return render(request, 'meteo.html', context=mydata)


def load_weather(codeCommune, weather):

    cityWeatherData = []
    cityWeatherDate = []
    cityWeatherTmin = []
    cityWeatherTmax = []

    # data from db
    wheatherData = Weather.objects.filter(codeInsee = codeCommune).values()

    # data from API
    forecastDate = weather['forecast']['datetime'][0:10]

    dateInDb = False

    if len(wheatherData) > 0:
       
        for data in wheatherData:
            if str(data['date']) == str(forecastDate):
                dateInDb = True

    # wheather already in db for that city at that date    
    if dateInDb:
        print('data already in db')

    # wheather not in db    
    else:

        # convert date format
        tmp_date = weather['forecast']['datetime'][0:10]
        my_date = datetime.strptime(tmp_date, '%Y-%m-%d')

        newWeatherData = Weather()
        newWeatherData.name = weather['city']['name']
        newWeatherData.codeInsee = weather['city']['insee']
        newWeatherData.date = my_date.date()
        newWeatherData.tmin = weather['forecast']['tmin']
        newWeatherData.tmax = weather['forecast']['tmax']
        newWeatherData.probarain = weather['forecast']['probarain']
        newWeatherData.save()

    cityWeather = Weather.objects.filter(codeInsee = codeCommune).order_by('date').values()
    
    for data in cityWeather:

        cityWeatherDate.append(str(data['date']))
        cityWeatherTmin.append(data['tmin'])
        cityWeatherTmax.append(data['tmax'])

    cityWeatherData.append(cityWeatherDate)
    cityWeatherData.append(cityWeatherTmin)
    cityWeatherData.append(cityWeatherTmax)

    return cityWeatherData


def load_regions(request):

    import requests
    import json

    regionNumb = 0
    regions_request = requests.get("https://geo.api.gouv.fr/regions")


    if len(Region.objects.all()) == 0:
        try:
            regions = json.loads(regions_request.content)
            regionNumb = len(regions)
        except Exception as e:
            regions = 'Error'

        for region in regions:
            newRegion = Region()
            newRegion.regionName = region['nom']
            newRegion.regionCode = region['code']
            newRegion.save()

    regionData = Region.objects.all().values()
    regionNumb = len(regionData)
    return render(request, 'home.html', {'regions': regionData, 'regionNumb': regionNumb })


def delete_regions(request):
    
    import requests
    import json

    Region.objects.all().delete()

    regionData = Region.objects.all().values()
    regionNumb = 0
    return render(request, 'home.html', {'regions': regionData, 'regionNumb': regionNumb })

