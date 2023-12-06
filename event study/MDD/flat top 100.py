import pandas as pd
import matplotlib.pyplot as plt


def mdd(data):
    return data['Ret'].std()


window = 5
data = pd.read_csv('8k_with_prices.csv')
data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])
data2 = pd.read_excel('100 worst drawdown.xlsx')
data2['Filing Date'] = pd.to_datetime(data2['Filing Date'])
dd = data.groupby(['Ticker', 'Filing Date']).apply(mdd).reset_index()
c = list(dd.columns)
c[-1] = 'std'
dd.columns = c
dd.sort_values(['std'], inplace=True)
ticker = []
fd = []
for i in range(len(dd)):
    if len(ticker) == 100:
        break
    t = dd['Ticker'].iloc[i]
    d = dd['Filing Date'].iloc[i]
    temp =data2[(data2['Ticker'] == t) & (data2['Filing Date'] == d)]
    if not len(temp):
        ticker.append(t)
        fd.append(d)
final = pd.DataFrame()
for i in range(len(ticker)):
    t = ticker[i]
    d = fd[i]
    temp = data[(data['Ticker'] == t) & (data['Filing Date'] == d)]
    final = pd.concat([final, temp], ignore_index=True)
final.to_excel('100 flat filings.xlsx')
