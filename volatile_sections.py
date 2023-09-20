import pandas as pd
import numpy as np


def lag_ret(data, lag):
    data = data.pct_change(periods=lag)
    return data.iloc[len(data) // 2 - 1]


def print_rank(ranking):
    for idx, x in enumerate(ranking):
        print("{i} th volatile is section {s}, with std {std}".format(i=idx + 1, s=x[1], std=x[0]))


data = pd.read_csv('data.csv')
data['section'] = data['section'].str.split(',')
data = data.explode('section', ignore_index=True)
data['section'] = data['section'].str.split('.')
lag = [1, 2, 5, 10]
section = list(range(1, 10))
for d in lag:
    res = []
    for s in section:
        temp_data = data[data['section'].apply(lambda x: x[0] == str(s))]
        if len(temp_data):
            ret = temp_data.groupby(['company', 'fillingdate'])['close'].apply(lag_ret, lag=d)
            res.append((np.std(ret.values, ddof=1), section.index(s)))
    res.sort(key=lambda x: x[0], reverse=True)
    print('lag {k}:'.format(k=d))
    print_rank(res)
