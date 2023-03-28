# -*- coding: utf-8 -*-
"""Capstone_Project ARIMA model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y2pxYpzAgJmHcHU8dJwiyWstpy7d5U5W
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

"""# **Data Exploration**"""

# Load the data
df = pd.read_excel('YTD_Attrition_2013_2023.xlsx')

df

df.shape

df.dtypes

df.isnull().sum()

df.columns

"""# **Data Preprocessing /Cleaning**"""

# Combine the year and month columns to create a new 'date' column
df['timestamp'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1)) + pd.offsets.MonthEnd(1)

# Drop the 'Year' and 'Month' columns
df.drop(['Year', 'Month'], axis=1, inplace=True)

print(df)

df.dtypes

#Check the missing values from dataframe

df.isna().sum()

"""# **Extra Steps for Learning purposes only. This step is unnecessary for Auto Arima Model.**"""

#Check if the YTD Attrition Rate Target Column is a Stationary or Non-Stationary data using Augmented Dickey-Fuller (ADF) Test
#This step is not necessary if we use model = pm.auto_arima since the auto_arima will automatically calculate and transform the data.

from statsmodels.tsa.stattools import adfuller
check_df = df['YTD Attrition Rate']
result = adfuller(check_df)

#this is just for reference purposed if we wish to do it manually.
# extract results
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))

"""Based on the above output, the ADF statistic for the test is -1.182228, and the p-value is 0.681194. The critical values at the 1%, 5%, and 10% levels are -3.492, -2.888, and -2.581, respectively.

To interpret the results, we can compare the ADF statistic to the critical values. If the ADF statistic is more negative than the critical values, we can reject the null hypothesis that the time series has a unit root, which suggests that the time series is stationary. Conversely, if the ADF statistic is less negative than the critical values, we cannot reject the null hypothesis, which suggests that the time series is non-stationary. 

In this case, the ADF statistic is greater than the critical values, so we cannot reject the null hypothesis that the time series has a unit root, and the time series is likely **non-stationary**.
"""

#This is just a reference if we wish to do it manually. But this step is unnecessary when using model = pm.auto_arima.

df["diff_1"] = df['YTD Attrition Rate'].diff(periods=1)
df["diff_2"] = df['YTD Attrition Rate'].diff(periods=2)
df["diff_3"] = df['YTD Attrition Rate'].diff(periods=3)
df = df.fillna(0.0000)
df

#Check the resulting ADF p-value after data transformation. This step is unnecessary when using model = pm.auto_arima.
result_diff1 = adfuller(df["diff_1"])

# extract results
print('ADF Statistic: %f' % result_diff1[0])
print('p-value: %f' % result_diff1[1])
print('Critical Values:')
for key, value in result_diff1[4].items():
    print('\t%s: %.3f' % (key, value))

#Plot the diff1. This step is unnecessary when using model = pm.auto_arima.
df['diff_1'].plot()

"""# **Visualizing the Data**"""

import plotly.express as px

fig = px.line(df, x='timestamp', y='YTD Attrition Rate', title='YTD Attrition Rate')

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(step="all")
        ])
    )
)
fig.show()

# Set the 'timestamp' column as the index of the DataFrame
df.set_index('timestamp', inplace=True)

df

df.plot(subplots=True)

print ("\nMissing values :  ", df.isnull().any())

"""# **Time Series** 
**ARIMA (AutoRegressive Integrated Moving Average) Model**

Data Period Jan 2013 - Feb 2023
"""

! pip install pmdarima

import pmdarima as pm

model = pm.auto_arima(df['YTD Attrition Rate'], 
                        m=12, seasonal=True,
                      start_p=0, start_q=0, max_order=4, test='adf',error_action='ignore',  
                           suppress_warnings=True,
                      stepwise=True, trace=True)

train=df[(df.index.get_level_values(0) >= '2012-12-31') & (df.index.get_level_values(0) <= '2020-12-31')]
test=df[(df.index.get_level_values(0) > '2020-12-31')]

train

test

model.fit(train['YTD Attrition Rate']) #univariate - taking only YTD attrition

forecast=model.predict(n_periods=50, return_conf_int=True) # forecast the next 50 months

print(forecast)

forecast_df = pd.DataFrame(forecast[0],index = test.index,columns=['Prediction'])

forecast_df

test

test_df = test['YTD Attrition Rate']

test_df

compare_df = pd.merge(forecast_df,test_df, on='timestamp')
compare_df.rename(columns={'YTD Attrition Rate': 'Actual'}, inplace=True)
compare_df['Diff'] = compare_df['Actual'] - compare_df['Prediction']

compare_df

#save the trained model

import pickle
with open('attrition_model.pkl', mode = 'wb') as pkl:
          pickle.dump(model,pkl)

"""# **Predict the future : Mar 2023 to Dec 2024**"""

forecast1=model.predict(n_periods=48, return_conf_int=True)

forecast_range=pd.date_range(start='2022-05-31', periods=32,freq='M')

forecast_range

forecast1_df = pd.DataFrame(forecast1[0],index =forecast_range,columns=['Prediction'])

forecast1_df

pd.concat([df['YTD Attrition Rate'],forecast1_df],axis=1).plot()

pd.concat([df['YTD Attrition Rate'],forecast_df],axis=1).plot()