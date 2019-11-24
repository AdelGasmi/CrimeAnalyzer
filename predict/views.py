
import os
import shutil
import uuid

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json
import numpy as np
import pandas as pd
from pandas import Series
from matplotlib import pyplot

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


from fbprophet import Prophet
import datetime
from visual.models import Crime
from django.db.models import Count

import matplotlib.pyplot as plt

listofCrimesGlobal = ['Agression', 'Violation de l ordre publique', 'Vol', 'Infractions relative aux armes',
                      'Vol de vehicule a  moteur', 'Autre infraction', 'Pratique deceptive', 'Dommage criminel', 'Transgression penale', 'Cambriolage',
                      'Harcelement', 'Agression sexuelle', 'Narcotique', 'Infraction sexuelle', 'Autre', 'Infraction d enfants', 'Kidnapping', 'Jeu d argent', 'Incendie volontaire',
                      'Violation des liee a l alcool', 'Obscenite', 'Non penal', 'indecence publique', 'Trafic humain', 'Violation de licence de trasport', 'Autre violation narcotique']

listOfRegionsGlobal = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                       '12', '13', '14', '15', '16', '17', '18', '19', '20', '22', '24', '25', '31']

listOfPlaceType = ['Appartement', 'Rue',
                   'Vehicule', 'Autre', 'Parking', 'Ecoles', 'Hopital', 'Restaurant/Cafe/Bar', 'Magasin', 'Gare', 'Banque', 'Stades', 'Hotel', 'Usine',
                   'Etablissement Etatique', 'Route', 'Lieu de culte', 'Aeroport', 'Rurale'
                   ]


# Create your views here.


def predictCrimes(request):

    type_Place = ['Appartement', 'Route', 'Etablissement', 'Local']
    motif = ['Revenge']
    context = {
        'crimes': listofCrimesGlobal,
        'regions': listOfRegionsGlobal,
        'places': listOfPlaceType
    }
    return render(request, 'predict/forecast.html', context)


def makeForecast(request):

    # # remove the directory to clear the files
    shutil.rmtree('static/visual/images/forecast')
    # # recreate the folder
    os.mkdir('static/visual/images/forecast')

    types = request.POST.getlist('types[]')
    regions = request.POST.getlist('regions[]')
    places = request.POST.getlist('places[]')
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    arrest = request.POST.getlist('arrest[]')
    period = request.POST['period']
    places = request.POST.getlist('places[]')
    # FbProphet parameters
    #modeAdditif = request.POST['modeAdditif']
    #modeMultiplicatif = request.POST['modeMultiplicatif']
    #print(modeAdditif, modeMultiplicatif)
    ordreHebdomadaire = request.POST['ordreHebdomadaire']
    ordreAnnuel = request.POST['ordreAnnuel']
    changepointPriorScale = request.POST['changepointPriorScale']
    seasonalityPriorScale = request.POST['seasonalityPriorScale']

    # holidays = request.POST.getlist('holidays[]')

    estimations = request.POST.getlist('estimations[]')

    # Filtering requested data
    df = pd.DataFrame(list(Crime.objects.filter(
        Date__range=[startDate, endDate], Primary_Type__in=types, District__in=regions, Arrest__in=arrest, Location_Description__in=places).values()))
    data = pd.DataFrame(df['Date'].value_counts(sort=False).reset_index())
    data.columns = ['ds', 'y']
    crimes = data.sort_values(by='ds')
    crimes.reset_index(inplace=True)
    crimes['ds'] = crimes.ds.astype(str)
    mode = ''

   # m = Prophet(n_changepoints=25, changepoint_range=0.8, yearly_seasonality='none', seasonality_mode='additive', seasonality_prior_scale=seasonalityPriorScale, changepoint_prior_scale=changepointPriorScale, weekly_seasonality=False, yearly_seasonality=False).add_seasonality(name="weekly", period=7, fourier_order=ordreHebdomadaire)
    m = Prophet(growth="linear", seasonality_mode="additive", changepoint_prior_scale=changepointPriorScale, seasonality_prior_scale=seasonalityPriorScale, yearly_seasonality=False).add_seasonality(
        name='yearly', period=365.25, fourier_order=ordreAnnuel).add_seasonality(name='weekly', period=7, fourier_order=ordreHebdomadaire)

    m = Prophet(seasonality_prior_scale=seasonalityPriorScale,
                changepoint_prior_scale=changepointPriorScale)
    m.fit(crimes)
    future = m.make_future_dataframe(periods=int(period))
    # making the forecast
    forecast = m.predict(future)

    path_components = 'static/visual/images/forecast/Prophet_Components' + \
        str(uuid.uuid4()) + '.png'
    m.plot_components(forecast).savefig(path_components)

    paths = {'path_components': path_components}

    # Calculate RMSE and MAPE using 10% of the dataset as a testing dataset
    size = len(crimes)
    test = forecast.iloc[-size:, :]
    rmse = np.sqrt(np.mean(np.square(test.yhat - crimes.y)))
    mape = np.mean(np.abs(test.yhat - crimes.y)/np.abs(crimes.y))

    metriques = {'rmse': rmse, 'mape': mape}

    # return json content for our crimes data and forecast
    crimes = crimes.to_dict(orient='records')
    forecast = forecast.to_dict(orient='records')

    return JsonResponse({'crimes': crimes, 'forecast': forecast, 'paths': json.dumps(paths), 'metriques': json.dumps(metriques)})


def showInstructions(request):

    return render(request, 'predict/instructions.html')
