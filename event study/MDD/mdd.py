import pandas as pd
import numpy as np

def mdd(data):
    Roll_Max = data['Close'].iloc[0]
    Daily_Drawdown = data['Close'] / Roll_Max - 1
    return Daily_Drawdown.min()


data = pd.read_csv('8k_with_prices_20days_back.csv')
data = data.assign(Section=data['Section'].str.split(',')).explode('Section', ignore_index=True)

data.drop_duplicates(inplace=True)
data.dropna(subset=['Close'], inplace=True)

data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])

data = data.groupby(['Ticker', 'Filing Date', 'Section']).apply(mdd).reset_index()
c = list(data.columns)
c[-1] = 'Maximum Drawdown'
data.columns = c
section = data['Section'].unique()
df = []
for s in section:
    temp = [s]
    temp_data = data[data['Section'] == s]
    temp.append(np.mean(temp_data['Maximum Drawdown']))
    temp.append(np.quantile(temp_data['Maximum Drawdown'], 0.25))
    temp.append(np.quantile(temp_data['Maximum Drawdown'], 0.5))
    temp.append(np.quantile(temp_data['Maximum Drawdown'], 0.75))
    df.append(temp)
df = pd.DataFrame(df)
df.columns = ['Section', 'Mean', '25', '50', '75']
df.sort_values(['Section'], inplace=True)
df.to_excel('NEW MDD result.xlsx')
