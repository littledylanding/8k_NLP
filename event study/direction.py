import pandas as pd
import numpy as np


def lag_ret(data, lag):
    data = data.pct_change(periods=lag)
    return data.iloc[len(data) // 2 - 1]


def pvalue(data, lag):
    ret = data.groupby(['company', 'fillingdate'])['close'].apply(lag_ret, lag=lag).values
    z = np.mean(ret) * np.sqrt(len(ret))/ np.std(ret, ddof=1)
    return True if abs(z) > 1.96 else False


data = pd.read_csv('data.csv')
data['section'] = data['section'].str.split(',')
data = data.explode('section', ignore_index=True)
items = []
lag = [1, 2, 5, 10]
res = []
for item in items:
    temp = []
    temp_data = data[data['section'] == item]
    for d in lag:
        temp.append('True') if pvalue(temp_data, d) else temp.append('False')
res = pd.DataFrame(np.array(res).T)
res.index = lag
res.columns = items
res.to_excel('result.xlsx')
