from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from urllib.parse import urlparse, parse_qs
from .models import Currency
from django.template import RequestContext

import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import base64
import datetime
import os
import random
import copy
import operator

src_data_folder = "./bitcoin/src/data/"
api_key = "981cba91d2064510972a06cf80dff1c6"

class CurrencyApi:

    def __init__(self) -> None:
        self.my_tools = MyTools()

    def loadcontentresponse(self, response):

        try:
            response_content = json.loads(response.content)
        except Exception as exception:
            response_content = None
            
        return response_content

    def getsupportedcurrency(self):
        
        # URL api - simulation depuis les premiers données retourné à partir des premières requête (sécurité anti-scrapping?)
        supported_currency_response = requests.get("https://api.currencyfreaks.com/supported-currencies")
        
        supported_currency = self.loadcontentresponse(supported_currency_response)

        now = self.my_tools.getstrtoday('%Y-%m-%d')

        if supported_currency != None:
            self.my_tools.savejsonfile(supported_currency, src_data_folder + 'supported_currency'+ "_" + now + '.')
            
        return supported_currency

    def getlatestrates(self):

        lastest_currency_rate_response = requests.get("https://api.currencyfreaks.com/latest?apikey=" + api_key )
        
        lastest_currency_rate = self.loadcontentresponse(lastest_currency_rate_response)

        now = self.my_tools.getstrtoday('%Y-%m-%d')

        if lastest_currency_rate != 'Error':
            self.my_tools.savejsonfile(lastest_currency_rate, src_data_folder + 'latest_currency_rate'+ "_" + now + '.')
            
        return lastest_currency_rate

class CurrencyDatabase:

    def __init__(self) -> None:
        self.my_tools = MyTools()
        self.currency_api = CurrencyApi()
        self.updatedatabase()
        

    def updatedatabase(self):

        # Pour éviter la duplication en base de donnée
        self.deleteallcurrencyobjectfromdatabase()
        
        # Charge les données du jour (api ou local si déjà présent)
        supported_currency = self.loadsupportedcurrency()
        latest_currency_rates = self.loadlatestcurrencyrates()
        
        # Mise à jour de la db
        self.savecurrencyondatabase(supported_currency,latest_currency_rates)

    def savecurrencyondatabase(self, supported_currencies, latest_currency_rates):
       
       # On va stocker un à uns les monnaies à partir des données chargés
        for supported_currency in supported_currencies:
            
            newcurrency = Currency()
            newcurrency.currencyCode = supported_currency['currencyCode']
            newcurrency.currencyName = supported_currency['currencyName']
            newcurrency.icon = supported_currency['icon']
            
            # Vu qu'on stocke un booleen coté db alors conversion
            if supported_currency['status'] == "AVAILABLE":
                newcurrency.status = True
            else:
                newcurrency.status = False
            
            # On formate les dates afin de les uniformiser pour une futur utilisation
            newcurrency.available_in_historical_data_from = self.my_tools.cleandatetime(supported_currency['available_in_historical_data_from'])
            newcurrency.available_in_historical_data_till = supported_currency['available_in_historical_data_till']
            
            newcurrency.countryCode = supported_currency['countryCode']
            newcurrency.countryName = supported_currency['countryName']
            
            # Toutes les monnaies, hormis le dollard américain, auront leur taux de change généré aléatoirement à partir de l'USD
            if not supported_currency['currencyCode'] == "USD":
                latest_currency_rates['base'] = supported_currency['currencyCode']
                new_currency_rates = copy.deepcopy(latest_currency_rates)
                
                # Modification des valeurs numériques dans le dictionnaire "rates"
                for key in new_currency_rates["rates"]:
                    new_currency_rates["rates"][key] = str(random.uniform(0, 100))
                
                newcurrency.currencyRates = new_currency_rates
            else:
                newcurrency.currencyRates = latest_currency_rates
            
            newcurrency.save()
            
        # Pour vérification on retourne le nombre d'objet stocké en base de donnée
        return Currency.objects.count()
        
    def loadsupportedcurrency(self):
        
        supported_currency_file_name = "supported_currency_" + self.my_tools.getstrtoday('%Y-%m-%d')
        supported_currency_file_path= os.path.join(src_data_folder, supported_currency_file_name + ".json")
        
        # Va lire les info sur l'api si le fichier du jour n'est pas présent
        if not os.path.isfile(supported_currency_file_path):
            return self.currency_api.getsupportedcurrency()
        else:
            return self.my_tools.readjsonfile(supported_currency_file_name)
        
    def loadlatestcurrencyrates(self):

        latest_currency_rate_file_name = "latest_currency_rate_" + self.my_tools.getstrtoday('%Y-%m-%d')
        latest_currency_rate_file_path= os.path.join(src_data_folder, latest_currency_rate_file_name + ".json")
        
        # Va lire les info sur l'api si le fichier du jour n'est pas présent
        if not os.path.isfile(latest_currency_rate_file_path):
            return self.currency_api.getlatestrates()
        else:
            return self.my_tools.readjsonfile(latest_currency_rate_file_name)
        
    def deleteallcurrencyobjectfromdatabase(self):
    
        return Currency.objects.all().delete()

class CurrencyChart:
    
    def __init__(self) -> None:
        pass

    def downloadcurrencychart(self, currency):
        
        # Créer un graphique avec Matplotlib
        fig = plt.figure()
        self.makecurrencychart(currency, fig)

        # Sauvegarder le graphique dans un objet BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Créer une réponse HTTP contenant le graphique
        response = HttpResponse(buffer, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="plot.png"'
        return response

    def createcurrencychart(self, currency_from, currency_to):
        
        # Créer un graphique avec Matplotlib
        fig = plt.figure()
        self.makecurrencychart(currency_from, currency_to, fig)

        # Sauvegarder le graphique dans un objet BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Ajouter l'image à un objet HttpResponse
        graphic = HttpResponse(image_png, content_type='image/png')
        
        return graphic

    def makecurrencychart(self, currency_from='USD', currency_to='EUR', fig=None):

        # Récupérer la monnaie
        currency_from_obj = Currency.objects.get(currencyCode=currency_from)

        # Récupérer les taux de change de la monnaie
        currency_from_rates = currency_from_obj.currencyRates

        # Obtenir les différents taux de change dans les dernières 24h [simulation aléatoire]
        date_currency = ['00h','02h','4h','6h','8h','10h','12h','14h','16h','18h','20h','22h',]
        value_currency = []

        for key, value in currency_from_rates['rates'].items():
            if key == currency_to:
                i = 0
                while i < len(date_currency):
                    i = i + 1
                    value_currency.append(random.uniform(float(value), float(value)+2))
                    print(value_currency)

        # Créer le graphique
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
           
        # Créer la légende
        fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
        ax.bar(date_currency, value_currency, color='b')
        ax.set_title('Taux de change de {} en {}'.format(currency_from, currency_to))
        ax.set_ylabel('Taux de change ({})'.format(currency_to), fontsize=11)
        ax.legend(['Taux de change de {} sur les dernières 24h'.format(currency_from)])
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.set_ylim(min(value_currency) - 0.1*min(value_currency), max(value_currency) + 0.1*max(value_currency))
        


    
class MyTools:

    def cleandatetime(self, string):
        
        date_list = string.replace("[", "").replace("]", "").split(", ")
        date_str_formatted = "-".join(date_list)
        
        return date_str_formatted
    
    def getstrtoday(self, format):
        
        return datetime.date.today().strftime(format)
    
    def savejsonfile(self, data, namefile):
    
        with open(src_data_folder + namefile + '.json', 'w') as file:
            json.dump(data, file)

    def readjsonfile(self, namefile):
    
        with open(src_data_folder + namefile + '.json', 'r') as file:
            json_data = json.load(file)
    
        return json_data
    

def display_chart(request):
    
    # On instancie la base de donnée avec les données les plus à jour
    currency_db = CurrencyDatabase()
    
    # Init
    currency_from_requested = None
    currency_to_requested = None
    value_convert_from_to = None
    image_chart = None
    
    # Par défaut retourne un graph avec les valeurs pour Dollar américain vers Euro 
    # car ce sont les seules valeurs extraitre de l'API vraissemblable
    if request.method == 'GET':
        if currency_from_requested == None:
            currency_from_requested = 'USD'
        
        if currency_to_requested == None:
            currency_to_requested = 'EUR'
    
        # Création du graph sous la forme d'une image affichable dans le template
        chart = CurrencyChart()
        mychart = chart.createcurrencychart(currency_from_requested, currency_to_requested)
        image_chart = base64.b64encode(mychart.content).decode('utf-8')
    
        # Conversion pour une unité de la monnaie A vers une monnaie B
        currency_ratio = Currency.objects.get(currencyCode=currency_from_requested)
        currency_from_rates = currency_ratio.currencyRates['rates'][currency_to_requested]
    
        value_convert_from_to = currency_from_rates  
    
    if request.method == 'POST':
        currency_from_requested = request.POST['currency_from']
        currency_to_requested = request.POST['currency_to']
        
        # Toujours valeur par défaut
        if currency_from_requested == None:
            currency_from_requested = 'USD'
        
        if currency_to_requested == None:
            currency_to_requested = 'EUR'
        
        if not currency_from_requested == currency_to_requested:
            # Création du graph sous la forme d'une image affichable dans le template
            chart = CurrencyChart()
            mychart = chart.createcurrencychart(currency_from_requested, currency_to_requested)
            image_chart = base64.b64encode(mychart.content).decode('utf-8')
        
            # Conversion pour une unité de la monnaie A vers une monnaie B
            currency_ratio = Currency.objects.get(currencyCode=currency_from_requested)
            currency_from_rates = currency_ratio.currencyRates['rates'][currency_to_requested]
        
            value_convert_from_to = currency_from_rates
        
    if value_convert_from_to == None:
        value_convert_from_to = "1"
        
    # On récupère tous les monnaies pour faire notre liste déroulante (à affiner)
    currencies = Currency.objects.all()
            

    
    mydata = {
        "imagechart": image_chart,
        "currencies": currencies,
        "currency_from": currency_from_requested,
        "currency_to": currency_to_requested,
        "value_convert_from_to": value_convert_from_to
    }
    
    return render(request, 'bitcoin.html', context=mydata)