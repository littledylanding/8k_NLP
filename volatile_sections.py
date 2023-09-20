import pandas as pd
import numpy as np


def lag_ret(data, lag):
    mid = len(data) // 2 - 1
    data = data.pct_change(periods=lag)
    return data.iloc[mid + lag]


def print_rank(ranking):
    for idx, x in enumerate(ranking):
        print("{i} th volatile is section {s}, with std {std}".format(i=idx + 1, s=x[1], std=x[0]))


data = pd.read_csv('8k_with_prices.csv')
data['Section'] = data['Section'].str.split(',')
data = data.explode('Section', ignore_index=True)
data['Section'] = data['Section'].str.split('.')
lag = [1, 2, 5, 10]
section = list(range(1, 10))
for d in lag:
    res = []
    for s in section:
        temp_data = data[data['Section'].apply(lambda x: x[0] == str(s))]
        if len(temp_data):
            ret = temp_data.groupby(['Ticker', 'Filing Date'])['Close'].apply(lag_ret, lag=d)
            res.append((np.std(ret.values, ddof=1), section.index(s)+1))
    res.sort(key=lambda x: x[0], reverse=True)
    print('lag {k}:'.format(k=d))
    print_rank(res)
