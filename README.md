# CrimeAnalyer web app

This is a snap shot of our project for the graduation as a Computer Science engineer in Data Science. 

This is a Django app that provides a solution for descriptive and predictive (timeseries forecasting) analysis for crimes data. 

Please take a look at the screen record of the example  [here](https://github.com/AdelGasmi/CrimeAnalyzer/tree/master/static/visual/assets/videos/) to have a look about some of the functionalities. 


For this snap shot, and for dev purposes (privacy of the data that we worked on), I tried to make a specific version for generic data 

## Data used

Because of the nature of the data of our final project, I used a public dataset that is available [HERE](https://www.kaggle.com/currie32/crimes-in-chicago).
 
## Timeseries forecasting

* [Google Collab Notebook](https://colab.research.google.com/drive/1dTPOm_nW5l_-_6untLYFwXQI308raoiS) - Colab notebook for the a detailed simulation and comparaison of timeseries forecasting techniques (Auto.SARIMA, ETS, and Facebook Prophet). 
PS: 
* You can check the notebook directly in this repository in [this file](https://github.com/AdelGasmi/CrimeAnalyzer/blob/master/timeseriesforecastingtechnique_statisticalmethods.ipynb)
* We did also a comparaison with LSTM working on our real data. Best results always went to Facebook Prophet on the daily level.

## Visualization
Actually, our solution is 80% based on visualizing data. For that, and using Javascript libraries (D3.Js, DC.Js, Plotly.Js, Leaflet.Js, etc.) combined with classification and clustering techniques in the backend (KMeans, Hierarchical clustering, and PCA ), we could offer many feautures in an interactive way. Take a look at our videos. 


## Building

It is best to use the python `virtualenv` tool to build locally with for example a version of python=3.6:

```sh
$ virtualenv-3.6 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ DEVELOPMENT=1 python manage.py runserver
```

Then visit `http://localhost:8000` to view the app. 

## requirements.txt

For the backend development. We used mainly the following python packages

```
Django==2.1.7
fbprophet==0.5
pandas==0.24.2
scikit_learn==0.21.2
matplotlib==2.2.2
numpy==1.14.3
```

