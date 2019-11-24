import pandas as pd
from pandas import Series
from matplotlib import pyplot
from fbprophet import Prophet
import numpy as np
import datetime

#df1 = pd.read_csv('Chicago_Crimes_2008_to_2011.csv')
df = pd.read_csv('Chicago_Crimes_2012_to_2017.csv')

df.head()

df['x'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p')

df['x2'] = df['x'].dt.strftime('%Y-%m-%d')

data = pd.DataFrame(df['x2'].value_counts(sort=False).reset_index())
data.columns = ['ds', 'y']
crimes = data.sort_values(by='ds')
crimes.reset_index(inplace=True)


# create a Prophet model
m = Prophet()

# fit the dataframe to the Prophet model
m.fit(crimes)

# create a new period to forecast
future = m.make_future_dataframe(periods=365)
future.head()

# making the forecast
forecast = m.predict(future)


# plotting the forecast
fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)
