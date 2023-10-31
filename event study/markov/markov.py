import pandas as pd
import numpy as np
from collections import defaultdict

eight_k_df = pd.read_csv('FilingData.csv')
eight_k_df.drop_duplicates(inplace=True)
eight_k_df['Filing Date'] = pd.to_datetime(eight_k_df['Filing Date'])
eight_k_df['Items'] = eight_k_df['Items'].str.replace(' ', '')
eight_k_df = eight_k_df.groupby(['Ticker', 'Filing Date']).agg({'Items': lambda x: ','.join(x)}).reset_index()
data = eight_k_df.assign(Items=eight_k_df['Items'].str.split(',')).explode('Items', ignore_index=True)
items = list(data['Items'].unique())
err = ['2.02101', '2.02104', '7.01104']
bad = ['1.03', '2.05', '5.01', '3.01']
for x in err:
    items.remove(x)
items = sorted([item for item in items if not isinstance(item, float) or not np.isnan(item)])
l1 = len(items)
l2 = len(bad)
Tickers = sorted(data['Ticker'].unique())
DF = []
res = np.zeros((l1, l1))
num = defaultdict(int)
for company in Tickers:
    data = eight_k_df[eight_k_df['Ticker'] == company].dropna().sort_values(by=['Filing Date'])
    for t in range(len(data) - 1):
        curr = data['Items'].iloc[t].split(',')
        next = data['Items'].iloc[t + 1].split(',')
        if (data['Filing Date'].iloc[t + 1] - data['Filing Date'].iloc[t]).days < 90:
            curr_idx = []
            next_idx = []
            for item in curr:
                if item in items:
                    num[item] += 1
                    curr_idx.append(items.index(item))
            for item in next:
                if item in items:
                    next_idx.append(items.index(item))
            for idx1 in curr_idx:
                for idx2 in next_idx:
                    res[idx1, idx2] += 1
        else:
            curr_idx = []
            for item in curr:
                curr_idx.append(items.index(item))
n = np.zeros(l1)
for i in range(l1):
    n[i] = num[items[i]]
n[n == 0] = 1
res /= n[:, None]
res = pd.DataFrame(res)
res.columns = res.index = items
res.to_excel('All items markov.xlsx')
res = res[bad]
res.to_excel('Bad items markov.xlsx')
