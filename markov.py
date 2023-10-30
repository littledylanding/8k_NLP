import pandas as pd
import numpy as np

eight_k_df = pd.read_csv('FilingData.csv')
eight_k_df.drop_duplicates(inplace=True)
eight_k_df['Filing Date'] = pd.to_datetime(eight_k_df['Filing Date'])
eight_k_df['Items'] = eight_k_df['Items'].str.replace(' ', '')
eight_k_df = eight_k_df.groupby(['Ticker', 'Filing Date']).agg({'Items': lambda x: ','.join(x)}).reset_index()
data = eight_k_df.assign(Items=eight_k_df['Items'].str.split(',')).explode('Items', ignore_index=True)
items = list(data['Items'].unique())
err = ['2.02101', '2.02104', '7.01104']
for x in err:
    items.remove(x)
items = sorted([item for item in items if not isinstance(item, float) or not np.isnan(item)])
l = len(items)
Tickers = data['Ticker'].unique()
DF = []
res = np.zeros((l, l))
for i in range(l):
    item_i = items[i]
    for j in range(i + 1, l):
        item_j = items[j]
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
                num[0, curr_idx] += 1
                num[1, next_idx] += 1
        row_sums = res.sum(axis=1).reshape(-1, 1)
        res /= row_sums
        temp_df = pd.DataFrame(res)
        temp_df = pd.concat([temp_df, pd.DataFrame(num[0, :])], axis=1, ignore_index=True)
        temp_df = pd.concat([temp_df, pd.DataFrame(list(num[1, :])+[np.nan]).transpose()], ignore_index=True)
        temp_df.index = temp_df.columns = [item_i, item_j, 'Both', 'Other', 'Frequency']
        DF.append(temp_df)
with pd.ExcelWriter('Markov.xlsx', engine='openpyxl') as writer:
    for df in DF:
        item_i, item_j = df.columns[0], df.columns[1]
        df.to_excel(writer, sheet_name=item_i + ' X ' + item_j)
