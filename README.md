# CrimeAnalyer Web App

This is a snap shot of our project for the graduation as a Computer Science engineer in Data Science. 

This is a Django app that provides a solution for descriptive and predictive (timeseries forecasting) analysis for crimes data. 

Please take a look at the screen record of the example  [here](https://github.com/AdelGasmi/CrimeAnalyzer/tree/master/static/visual/assets/videos/) to have a look about some of the functionalities. 


For this snap shot, and for dev purposes (privacy of the data that we worked on), I tried to make a specific version for generic data 

## Data Used

Because of the nature of the data of our final project, I used a public dataset that is available [HERE] (https://www.kaggle.com/currie32/crimes-in-chicago).
 
## Timeseries

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - Colab notebook for the a detailed simulation and comparaison of timeseries forecasting techniques. 
PS: You can check the notebook directly in this repository in [this file](https://github.com/AdelGasmi/CrimeAnalyzer/blob/master/timeseriesforecastingtechnique_statisticalmethods.ipynb)




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

