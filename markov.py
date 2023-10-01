import pandas as pd
import numpy as np

eight_k_df = pd.read_excel('FilingData.xlsx')
eight_k_df.drop_duplicates(inplace=True)
eight_k_df['Filing Date'] = pd.to_datetime(eight_k_df['Filing Date'])
eight_k_df['Section'] = eight_k_df['Section'].str.replace('Item ', '')
eight_k_df['Section'] = eight_k_df['Section'].str.replace(' ', '')
data = eight_k_df.assign(Section=eight_k_df['Section'].str.split(',')).explode('Section', ignore_index=True)
items = data['Section'].unique()
items = sorted([item for item in items if not isinstance(item, float) or not np.isnan(item)])
l = len(items)
Tickers = data['Ticker'].unique()
DF = []
for i in range(l):
    item_i = items[i]
    for j in range(i + 1, l):
        item_j = items[j]
        res = np.zeros((4, 4))
        for company in Tickers:
            data = eight_k_df[eight_k_df['Ticker'] == company].dropna().sort_values(by=['Filing Date'])
            for t in range(len(data)-1):
                curr = data['Section'].iloc[t].split(',')
                next = data['Section'].iloc[t+1].split(',')
                if item_i in curr and item_j in curr:
                    curr_idx = 2
                elif item_i in curr:
                    curr_idx = 0
                elif item_j in curr:
                    curr_idx = 1
                else:
                    curr_idx = 3
                if item_i in next and item_j in next:
                    next_idx = 2
                elif item_i in next:
                    next_idx = 0
                elif item_j in next:
                    next_idx = 1
                else:
                    next_idx = 3
                res[curr_idx, next_idx] += 1
        row_sums = res.sum(axis=1).reshape(-1, 1)
        res /= row_sums
        temp_df = pd.DataFrame(res)
        temp_df.index = temp_df.columns = [item_i, item_j, 'Both', 'Other']
        DF.append(temp_df)
with pd.ExcelWriter('Markov.xlsx', engine='openpyxl') as writer:
    for df in DF:
        item_i, item_j = df.columns[0], df.columns[1]
        df.to_excel(writer, sheet_name=item_i + ' X ' + item_j)
