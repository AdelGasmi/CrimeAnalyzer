import json
import os
import shutil
import uuid

from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
import pandas as pd
import numpy as np
from visual.models import Crime
from django.db.models import Count, Sum, IntegerField
from django.db.models.functions import Cast
from datetime import datetime
from sklearn.preprocessing import StandardScaler

from sklearn.cluster import KMeans, AgglomerativeClustering
#from statsmodels.tsa.seasonal import seasonal_decompose
from django.contrib.auth.decorators import login_required


from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt
from random import randint


listofCrimesGlobal=['Agression','Violation de l ordre publique','Vol','Infractions relative aux armes',
'Vol de vehicule a  moteur','Autre infraction','Pratique deceptive','Dommage criminel','Transgression penale','Cambriolage',
'Harcelement','Agression sexuelle','Narcotique','Infraction sexuelle','Autre','Infraction d enfants','Kidnapping','Jeu d argent','Incendie volontaire',
'Vilation des liee a l alcool','Obscenite','Non penal','indecence publique','Trafic humain','Violation de licence de trasport','Autre violation narcotique']

listOfRegionsGlobal = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','22','24','25','31']


@login_required
def showLandingPage(request):
    return render(request, 'visual/landing.html')


@login_required
def index(request):
    template = loader.get_template('visual/starter.html')
    context ={
        'var': "simple text",
    }
    return HttpResponse(template.render(context,request))

@login_required
def allDataPage(request):
    return render(request, 'visual/allData.html')

@login_required()
def resumedData(request):

    allData = pd.DataFrame(list(Crime.objects.all().values('Date','Primary_Type','District').annotate(crimes_Count=Count('id')).order_by('Date')))
    print(type(allData))
    allData["Date"] = allData["Date"].apply(lambda x: x.strftime('%Y-%m-%d'))
    #allData['Date'] = allData['Date'].dt.strftime('%Y-%m-%d')
    #allData['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
    #print(type(allData))
    #allData['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    jsonData = allData.to_dict(orient='records')
    #print(jsonData)
    return JsonResponse({'data': jsonData})

@login_required
def showMap(request):
    global listofCrimesGlobal
    listOfCrimes = listofCrimesGlobal
    listOfRegions = listOfRegionsGlobal
    context = {
        'crimes': listOfCrimes,
        'regions': listOfRegions,
    }
    return render(request, 'visual/mapNormal.html', context)

@login_required
def cluster(request):
    listOfRegions = listOfRegionsGlobal
    context = {

        'regions': listOfRegions,
    }
    return render(request,'visual/clustering.html', context)

def cluster_district(request):
    listOfCrimes = listofCrimesGlobal
    listOfRegions = listOfRegionsGlobal
    context = {
        'crimes': listOfCrimes,
        'regions': listOfRegions,
    }
    return render(request, 'visual/districts_cluster.html', context)

@login_required
def showHeatMap(request):
    global listofCrimesGlobal
    listOfCrimes = listofCrimesGlobal
    listOfRegions = listOfRegionsGlobal
    context = {
        'crimes': listOfCrimes,
        'regions' : listOfRegions
    }
    return render(request, 'visual/heatMap.html', context)


@login_required
def compareCrimes(request):
    global listofCrimesGlobal
    listOfCrimes = listofCrimesGlobal
    context = {
        'crimes': listOfCrimes
    }
    return render(request, 'visual/comapre.html', context)


dateSelected = 2016
typesSelected = ['all']


def getData(request):
    global dateSelected
    dateSelected= request.POST['date']
    global typesSelected
    typesSelected = request.POST.getlist('crime_type')
    crime = Crime.objects.get(id=1)
    print('hello ',crime.Date, ' id =1')
    return redirect('home/')


def getDataPerYear( year, types):
    df = pd.read_csv('data/./2016CrimesAlgiers.csv', nrows=2000)
    #cols_to_keep = ['Date', 'Primary Type', 'Arrest', 'Longitude', 'Latitude']
    df = df.dropna()
    if 'all' not in types:
        df = df[df['Primary Type'].isin(types)]
    #df['d'] = pd.to_datetime(df.Date).dt.date.astype(str)
    #df['Date'] = pd.to_datetime(df.Date)
    #df = df[df.Date.dt.year == year]
    #df = df.drop('Date', axis= 1)
    return df.to_json(orient='records')

def filterData(request):
    types = request.POST.getlist('types[]')
    regions = request.POST.getlist('regions[]')
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    arrest = request.POST.getlist('arrest[]')
    print(startDate, endDate, arrest, types)
    rawData = Crime.objects.filter(Date__range=[startDate, endDate], Arrest__in=arrest, Primary_Type__in=types, District__in=regions)
    result = []
    for i in rawData.values():
        i['Date'] = i['Date'].strftime('%m/%d/%Y')
        result.append(i)


    #for record in rawData:
        #json_obj = dict(date = record.Date, arrest= record.Arrest, type= record.Primary_Type)
        #result.append(json_obj)

    #response = serializers.serialize('json',result)
    #return HttpResponse(json.dumps(json_obj),content_type='application/json')

    #return HttpResponse(rawData, content_type='application/json')

    return HttpResponse(json.dumps(result))
#for crime comparaison
def customFilter(request):
    types = request.POST.getlist('types[]')
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    arrest = request.POST.getlist('arrest[]')
    rawData = Crime.objects.filter(Date__range=[startDate, endDate], Arrest__in=arrest, Primary_Type__in=types).\
        values('Date','Primary_Type').\
        annotate(crimes_Count=Count('id')).order_by('Date')

    result = []
    for i in rawData:
        #i['Date'] = i['Date'].strftime('%m/%d/%Y')
        i['Date'] = i['Date'].strftime('%Y-%m-%d')
        result.append(i)

    myDict = {}
    for i in types:
        myDict[i]= []

    dfGlobal = pd.DataFrame(result)

    for index, row in dfGlobal.iterrows():
        myDict[row['Primary_Type']].append(row['crimes_Count'])
    toDelete = []


    for element in myDict:
        if not myDict[element]:
            toDelete.append(element)

    if toDelete:
        for x in toDelete:
            myDict.pop(x)

    sizes = []
    for element in myDict:
        sizes.append(len(myDict[element]))
    minSize = min(sizes)

    resultCorr = {}
    myDict1 =myDict.copy()
    #finding correlation using numpy
    for c in myDict:
        myDict1.pop(c)
        for l in myDict1:
            a = np.array(myDict[l])[0:minSize-1]
            b = np.array(myDict[c])[0:minSize-1]
            resultCorr[c+' <> '+l] = np.corrcoef(a,b)[0][1]

    #for serie in myDict:
        #resultTrend = seasonal_decompose(serie, model='additive')
        #print(resultTrend.trend)

    return HttpResponse(json.dumps({'result':result, 'corr':resultCorr}))

#get insights from timeseries data
def findInsightsTS(request):
    types = request.POST.getlist('types[]')
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    arrest = request.POST.getlist('arrest[]')
    rawData = Crime.objects.filter(Date__range=[startDate, endDate], Arrest__in=arrest, Primary_Type__in=types). \
        values('Date'). \
        annotate(crimes_Count=Count('id')).order_by('Date')
    result = []
    for i in rawData:
        i['Date'] = i['Date'].strftime('%m/%d/%Y')
        result.append(i)
    df = pd.DataFrame(result)
    df.set_index('Date')
    print(df)
    return HttpResponse('hello')


def default(request):
    print(dateSelected, typesSelected)
    return HttpResponse(getDataPerYear(dateSelected,typesSelected))

from users.models import Settings
from django.contrib.auth.models import User

def defaultHome(request):

    #userLogged = request.user
    #limit = Settings.objects.filter(user=userLogged).values('limit')
    #settings = User.objects.get(username=request.user).Settings
    s = User.objects.select_related("settings").get(username=request.user).settings
    print(s.limit)
    rawData = Crime.objects.filter(Date__range=['2016-01-01', '2016-12-31']).order_by('Date')[:s.limit]
    result = []
    for i in rawData.values():
        i['Date'] = i['Date'].strftime('%m/%d/%Y')
        result.append(i)
    return HttpResponse(json.dumps(result))


def customeHome(request):
    startDate  = request.POST['startDate']
    endDate = request.POST['endDate']
    rawData = Crime.objects.filter(Date__range=[startDate, endDate]).order_by('Date')
    result = []
    for i in rawData.values():
        i['Date'] = i['Date'].strftime('%m/%d/%Y')
        result.append(i)
    return HttpResponse(json.dumps(result))

#makeClustering for crimes
def makeKmeans(request):
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']
    regions = request.POST.getlist('regions[]')
    arrest = request.POST.getlist('arrest[]')
    numberCluster = request.POST['numberClusters']
    numberTests = request.POST['numberEssais']
    numberIterations = request.POST['numberIterations']
    numberClustersHi = request.POST['numberClustersHi']

    df1 = pd.DataFrame(list(Crime.objects.filter(Date__range=[startDate, endDate], Arrest__in=arrest, District__in=regions).values('Primary_Type')
                            .annotate(count=Count('id'))))

    allTypes = df1['Primary_Type'].unique()
    #df1['arrested'] = 0
    #df1['not_arrested'] = 0

    for index,row in df1.iterrows():
        f = Crime.objects.filter(Primary_Type=row['Primary_Type'], Arrest=True).count()
        ff = (f/row['count'])
        df1.at[index, 'arrested'] = ff
        df1.at[index, 'not_arrested'] = 1- ff

    to_analyze  = df1[['count','arrested','not_arrested']]
    clusters_kmeans = KMeans(n_clusters=int(numberCluster), n_init=int(numberTests), max_iter=int(numberIterations))
    clusters_kmeans.fit(to_analyze)
    clusters_kmeans.cluster_centers_
    result_kmeans = clusters_kmeans.labels_
    to_return_Kmeans = {}
    for i in range(0,int(numberCluster)):
        to_return_Kmeans[i] = []

    for i, item in enumerate(result_kmeans):
        to_return_Kmeans[item].append(allTypes[i])



    # clustering hiearchique
    if numberClustersHi:
        clusters_hiearchique = AgglomerativeClustering(int(numberClustersHi)).fit(to_analyze)
    else:
        clusters_hiearchique = AgglomerativeClustering().fit(to_analyze)

    result_hiearchique = clusters_hiearchique.labels_

    to_return_Hi = {}
    for i in range(0, len(np.unique(result_hiearchique))):
        to_return_Hi[i] = []

    for i, item in enumerate(result_hiearchique):
        to_return_Hi[item].append(allTypes[i])



    return HttpResponse(json.dumps({'hi':to_return_Hi,'kmeans':to_return_Kmeans}))

def clusterDistricts(request):
    #remove the directory to clear the files
    shutil.rmtree('static/visual/images/graphs')
    #recreate the folder
    os.mkdir('static/visual/images/graphs')

    types = request.POST.getlist('types[]')
    regions = request.POST.getlist('regions[]')
    startDate = request.POST['startDate']
    endDate = request.POST['endDate']

    k = int(request.POST['numberClusters'])

    df = pd.DataFrame(list(Crime.objects.filter(Date__range=[startDate, endDate], Primary_Type__in=types, District__in=regions)
                           .values('Case_Number','Primary_Type','District')
                            .annotate(count=Count('id'))))
    crimeArray = df.groupby(['Primary_Type', 'District'])['District'].count().unstack()
    crimeArray = crimeArray.transpose()
    crimeArray = crimeArray.replace(np.nan, 0)

    #PCA analysis
    pca = PCA()
    crimePCA = pca.fit(scale(crimeArray))
    cumsum = crimePCA.explained_variance_ratio_.cumsum()

    with plt.style.context('seaborn-whitegrid'):
        plt.figure(figsize=(6, 4))

        font = {'weight': 'bold',
                'size': 18}

        plt.rc('font', **font)

        plt.plot(range(1, len(cumsum) + 1), cumsum, '-o', color='b')
        plt.xlabel('Composante principale')
        plt.ylabel('Taux d information')
        plt.tight_layout()


    #creating of path with unique id
    pathPCAresult = 'static/visual/images/graphs/pca_results'+str(uuid.uuid4())+'.png'
    plt.savefig(pathPCAresult)

    pcDF = pd.DataFrame(crimePCA.components_[0:4])
    pcDF = pcDF.transpose()
    pcDF.columns = ['PC1', 'PC2', 'PC3', 'PC4']
    pcDF_copy = pcDF.copy()
    indexes = crimeArray.columns.tolist()
    pcDF.index = [indexes]

    PCAtableJSON = pcDF_copy.to_json(orient="records")
    types  = json.dumps(indexes)


    crimeProject = pca.fit_transform(scale(crimeArray))
    sector = crimeArray.index.tolist()

    crime2 = np.array(crimeProject[0, 0:2])
    for i in range(1, len(sector)):
        crime2 = np.vstack([crime2, crimeProject[i, 0:2]])

    #finding the optimal number of clusters
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(crime2)
    cluster_range = range(1, 20)
    cluster_errors = []

    for num_clusters in cluster_range:
        clusters = KMeans(num_clusters)
        clusters.fit(X_scaled)
        cluster_errors.append(clusters.inertia_)

    clusters_df = pd.DataFrame({"num_clusters": cluster_range, "cluster_errors": cluster_errors})

    plt.style.context('seaborn-whitegrid')
    plt.figure(figsize=(6, 4))
    font = {'weight': 'bold','size': 18}
    plt.rc('font', **font)
    plt.plot(clusters_df.num_clusters, clusters_df.cluster_errors, marker="o")
    plt.xlabel('N cluster')
    plt.ylabel('Erreur')
    plt.tight_layout()
    pathOptimalNumberOfClusters = 'static/visual/images/graphs/optimal' + str(uuid.uuid4()) + '.png'
    plt.savefig(pathOptimalNumberOfClusters)


    kmeans = KMeans(n_clusters=k, random_state=123, n_init=10).fit_predict(crime2)

    colors = []
    for i in range(k):
        colors.append('#%06X' % randint(0, 0xFFFFFF))

    kcolors = []
    for i in kmeans:
        kcolors.append(colors[i])

    h = .02
    x_min, x_max = crime2[:, 0].min() - 1, crime2[:, 0].max() + 1
    y_min, y_max = crime2[:, 1].min() - 1, crime2[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    kmesh = KMeans(n_clusters=k, random_state=123, n_init=10)
    kmesh.fit(crime2)

    kmeshPredict = kmesh.predict(np.c_[xx.ravel(), yy.ravel()])
    kmeshPredict = kmeshPredict.reshape(xx.shape)

    with plt.style.context('seaborn-whitegrid'):
        plt.figure(figsize=(8, 8))

        font = {'weight': 'bold',
                'size': 22}

        plt.rc('font', **font)

        plt.imshow(kmeshPredict, interpolation='nearest',
                   extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                   cmap=plt.cm.Paired, aspect='auto', origin='lower')

        for i, labels in enumerate(sector):
            plt.scatter(crime2[i, 0], crime2[i, 1], s=250, color=kcolors[i])
            plt.annotate(labels, (crime2[i, 0], crime2[i, 1]))

        plt.xlabel('Composante principale 1')
        plt.ylabel('Composante principale 2')
        plt.tight_layout()

    #creation of unique id for cluster result image
    pathClusterResult = 'static/visual/images/graphs/cluster_results' + str(uuid.uuid4()) + '.png'
    plt.savefig(pathClusterResult)
    #to avoid an error with plt
    plt.close('all')
    #regrouping paths in one dictionary
    paths = {'pcaResult': pathPCAresult, 'clusterResult': pathClusterResult, 'numberClusters': pathOptimalNumberOfClusters}


    #labels = json.dumps(kmesh.labels_)
    #dic_labels = {}
    #dic_labels['labels'] = kmesh.labels_
    labels = pd.Series(kmesh.labels_).to_json(orient='values')
    labels_before = list(pd.Series(kmesh.labels_))
    regions = json.dumps(sector)

    #associate each region with its color
    districtsColorsDic = {}

    for i in range(len(sector)):
        print(i)
        districtsColorsDic[sector[i]] = colors[labels_before[i]]


    return JsonResponse({'data': PCAtableJSON, 'types': types, 'paths': json.dumps(paths),
                         'labels': labels, 'regions': regions, 'colors': colors, 'regionsColord': json.dumps(districtsColorsDic) })


