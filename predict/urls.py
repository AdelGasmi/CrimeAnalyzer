from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('make/', views.predictCrimes, name='showForecast'),
    url(r'^makeForecast', views.makeForecast, name="makeForecast"),
    path('instructions/', views.showInstructions, name='showInstructions'),
    #path('instructions/', views.showInstructions, name='instructions'),
]
