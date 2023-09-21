import pandas as pd
import numpy as np


def lag_ret(data, lag):
    data = data.pct_change(periods=lag)
    return data.iloc[len(data)//2-1+lag]


def pvalue(data, lag):
    ret = data.groupby(['Ticker', 'Filing Date'])['Close'].apply(lag_ret, lag=lag).values
    z = np.mean(ret) * np.sqrt(len(ret)) / np.std(ret, ddof=1)
    return True if abs(z) > 1.96 else False, z


data = pd.read_csv('/Users/jiaqiding/Desktop/8k_NLP/8k_with_prices.csv')
data['Section'] = data['Section'].str.split(',')
data = data.explode('Section', ignore_index=True)
items = ['3.02', '8.01']
lag = [1, 2, 5, 10]
res = []
res2 = []
for item in items:
    temp = []
    temp2 = []
    temp_data = data[data['Section'] == item]
    for d in lag:
        temp.append('True') if pvalue(temp_data, d)[0] else temp.append('False')
        temp2.append(pvalue(temp_data, d)[1]) if pvalue(temp_data, d)[0] else temp2.append(pvalue(temp_data, d)[1])
    res.append(temp)
    res2.append(temp2)
res = pd.DataFrame(np.array(res).T)
res.index = lag
res.columns = items
res.to_excel('Truth.xlsx')
res2 = pd.DataFrame(np.array(res2).T)
res2.index = lag
res2.columns = items
res2.to_excel('zValue.xlsx')

