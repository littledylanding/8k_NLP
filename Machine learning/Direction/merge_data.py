import pandas as pd
import numpy as np


data1 = pd.read_excel('bagofwords.xlsx')
data2 = pd.read_csv('filtered_data.csv')
data3 = pd.read_csv('Pricein&out.csv').drop_duplicates()
data1 = data1[data1.columns[:9]]
data1 = data1.dropna()
data1 = data1[data1['Negative'].apply(lambda x: not isinstance(x, str))]
data1['Filing Date'] = pd.to_datetime(data1['Filing Date'])
data2['Filing Date'] = pd.to_datetime(data2['Filing Date'])
data3['Filing Date'] = pd.to_datetime(data3['Filing Date'])

data = data1.merge(data2, on=['Ticker', 'Filing Date'])
data = data.merge(data3, on=['Ticker', 'Filing Date'])
data.dropna(inplace=True)
data.to_csv('Final.csv')
