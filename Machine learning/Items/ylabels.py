import pandas as pd

bad = ['1.03', '2.05', '5.01', '3.01']


def get_next_rows_within_90_days(row, data):
    df = data.copy(deep=True)
    df['Items'] = df['Items'].str.split(',')
    current_datetime = row.name
    end_datetime = current_datetime + pd.Timedelta(days=30)
    next_items = []
    start_idx = df.index.get_loc(current_datetime) + 1
    for idx in range(start_idx, len(df)):
        if df.index[idx] > end_datetime:
            break
        next_items.extend(df.iloc[idx]['Items'])
    for item in bad:
        if item in next_items:
            return 1
    return 0


data = pd.read_csv('filtered_data.csv')
data['Filing Date'] = pd.to_datetime(data['Filing Date'])
tickers = data['Ticker'].unique()
res = pd.DataFrame()
for ticker in tickers:
    temp = data[data['Ticker'] == ticker].dropna().sort_values(by=['Filing Date'])
    temp.set_index('Filing Date', inplace=True)
    temp['y'] = temp.apply(lambda row: get_next_rows_within_90_days(row, temp), axis=1)
    res = pd.concat([res, temp], ignore_index=True)
print(res['y'].sum())
res.to_csv('Data.csv')