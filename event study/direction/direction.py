import pandas as pd
import numpy as np
from scipy.stats import norm


def lag_ret(data, lag):
    return data.iloc[len(data) // 2 - 1 + lag]


def pvalue(data, lag):
    ret = data.groupby(['Ticker', 'Filing Date'])['Ret'].apply(lag_ret, lag=lag).dropna()
    z = np.mean(ret) / (np.std(ret, ddof=1) / np.sqrt(len(ret)))
    if z > norm.ppf(0.95):
        indicator = 'up'
    elif z < norm.ppf(0.05):
        indicator = 'down'
    else:
        indicator = 'zero'
    return indicator, z


data = pd.read_csv('8k_with_prices.csv')
data = data.assign(Items=data['Items'].str.split(',')).explode('Items', ignore_index=True)
data.drop_duplicates(inplace=True)

data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values(by=['Ticker', 'Filing Date', 'Date'])

items = data['Items'].unique()
items = sorted([item for item in items if not isinstance(item, float) or not np.isnan(item)])
lag = [1, 2, 5, 10]
res = []
res2 = []
for item in items:
    temp = []
    temp2 = []
    temp_data = data[data['Items'] == item]
    for d in lag:
        indicator, z = pvalue(temp_data, d)
        temp.append(indicator)
        temp2.append(z)
    res.append(temp)
    res2.append(temp2)
for item in items:
    temp_data = data[data['Items'] == item]


res = pd.DataFrame(np.array(res).T)
res.index = lag
res.columns = items
res.to_excel('Truth.xlsx')
res2 = pd.DataFrame(np.array(res2).T)
res2.index = lag
res2.columns = items
res2.to_excel('zValue.xlsx')

