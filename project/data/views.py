from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import RequestContext
from .models import Region

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
        "df" : ['nico', 'lui', 'lolo'],
        'df1': [1, 4, 8],
        'regions': regionData, 
        'departements': departments, 
        'regionNumb': regionNumb,
        'departmentNumb' : departmentNumb,
        'regionData' : regionData,
        'regionInfo' : regionInfo,
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
        'nom': departmentNom,
        'code': departmentCode,
        'population': population,
        'cityNumb': cityNumb,
    }
    # print(result)
    return result


def about(request):
    return render(request, 'about.html', {})


def addVisitedRegion(request):
    import requests
    import json
    regionNumb = 0

    region_instance = Region.objects.create(regionName='test', regionCode=33, regionVisited=True)

    regions_request = requests.get("https://geo.api.gouv.fr/regions")
    
    try:
        regions = json.loads(regions_request.content)
        regionNumb = len(regions)
    except Exception as e:
        regions = 'Error'

    return render(request, 'home.html', {'regions': regions, 'regionNumb': regionNumb })


def retrieveRegion(request):
    regions = Region.objects.all()
    regionNumb = len(regions)
    return render(request, 'home.html', {'regions': regions, 'regionNumb': regionNumb })



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
            newRegion.regionVisited = False
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