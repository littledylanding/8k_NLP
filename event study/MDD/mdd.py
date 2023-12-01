import pandas as pd
import numpy as np


def mdd(data):
    mid = len(data) // 2
    Roll_Max = data['Close'].iloc[mid-2:mid+3].cummax()
    Daily_Drawdown = data['Close'].iloc[mid-2:mid+3]/ Roll_Max - 1
    return Daily_Drawdown.min()


data = pd.read_csv('8k_with_prices.csv')
data = data.assign(Items=data['Items'].str.split(',')).explode('Items', ignore_index=True)

data.drop_duplicates(inplace=True)
data.dropna(subset=['Close'], inplace=True)

data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])

data = data.groupby(['Ticker', 'Filing Date', 'Items']).apply(mdd).reset_index()
c = list(data.columns)
c[-1] = 'Maximum Drawdown'
data.columns = c
section = list(data['Items'].unique())
err = ['2.02101', '2.02104', '7.01104']
for x in err:
    section.remove(x)
df = []
for s in section:
    temp = [s]
    temp_data = data[data['Items'] == s]
    temp.append(np.mean(temp_data['Maximum Drawdown']))
    temp.append(np.quantile(temp_data['Maximum Drawdown'], 0.25))
    temp.append(np.quantile(temp_data['Maximum Drawdown'], 0.5))
    temp.append(np.quantile(temp_data['Maximum Drawdown'], 0.75))
    df.append(temp)
df = pd.DataFrame(df)
df.columns = ['Items', 'Mean', '25', '50', '75']
df.sort_values(['Items'], inplace=True)
df.to_excel('NEW MDD result.xlsx')
