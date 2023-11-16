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


window = 10
data = pd.read_pickle('df_item_sp600_daily_return_1106.pkl')
data = data.assign(Items=data['Items'].str.split(', ')).explode('Items', ignore_index=True)
data.drop_duplicates(inplace=True)

data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values(by=['Ticker', 'Filing Date', 'Date'])
data = data.groupby(['Accession Number', 'Items']).filter(lambda x: len(x) == 2 * window + 1).reset_index(drop=True)

items = data['Items'].unique()
items = sorted([item for item in items if not isinstance(item, float) or not np.isnan(item)])
err = ['2.02101', '2.02104', '7.01104']
for x in err:
    if x in items:
        items.remove(x)
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
