import pandas as pd


def get_one_columns(row):
    return ', '.join(row.index[row == 1].tolist())


data1 = pd.read_csv('filtered_data.csv')
data1 = data1[[x for x in data1.columns if 'LSM' not in x]]
data1['Items'] = data1.apply(get_one_columns, axis=1)
data1 = data1[data1.columns[[0, 1, -1]]]
data1['Filing Date'] = pd.to_datetime(data1['Filing Date'])
data2 = pd.read_pickle('df_item_full_sp600.pkl')[['Ticker', 'Date', 'Items']]
data2.rename(columns={'Date': 'Filing Date'}, inplace=True)
data = pd.concat([data1, data2], ignore_index=True, axis=0)
data.sort_values(['Ticker', 'Filing Date'], inplace=True)
data.to_csv('FilingData.csv')
