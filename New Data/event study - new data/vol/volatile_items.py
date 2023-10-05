import pandas as pd
import numpy as np

def lag_ret(data, lag):
    mid = len(data) // 2 - 1
    data = data.pct_change(periods=lag)
    return data.iloc[mid + lag]

def print_rank(ranking):
    for idx, x in enumerate(ranking):
        print("{i} th volatile is section {section}, with std {std}".format(i=idx + 1, section=x[1], std=x[0]))

data = pd.read_csv('8k_with_prices.csv')
data = data.assign(Section=data['Section'].str.split(',')).explode('Section', ignore_index=True)

data.drop_duplicates(inplace=True)
data.dropna(subset=['Close'], inplace=True)

data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])

grouped = data.groupby(['Ticker', 'Filing Date', 'Section'])
data = grouped.filter(lambda x: len(x) >= 21).reset_index(drop=True)

lag = [1, 2, 5, 10]
sections = list(data['Section'].unique())

for d in lag:
    res = []
    for section in sections:
        temp_data = data[data['Section'] == section]
        if len(temp_data):
            ret = temp_data.groupby(['Ticker', 'Filing Date'])['Close'].apply(lag_ret, lag=d)
            res.append((np.std(ret.values, ddof=1), section))
    res.sort(key=lambda x: x[0], reverse=True)
    print('lag {k}:'.format(k=d))
    print_rank(res)
