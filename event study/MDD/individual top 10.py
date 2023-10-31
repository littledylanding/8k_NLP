import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def mdd(data):
    Roll_Max = data['Close'].iloc[9]
    Daily_Drawdown = data['Close'].iloc[9:] / Roll_Max - 1
    return Daily_Drawdown.min()


data = pd.read_csv('8k_with_prices.csv')

data.drop_duplicates(inplace=True)
data.dropna(subset=['Close'], inplace=True)

data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])
data = data[(data['Filing Date'] < pd.to_datetime('2020-02-01')) | (data['Filing Date'] > pd.to_datetime('2020-03-31'))]
dd = data.groupby(['Ticker', 'Filing Date']).apply(mdd).reset_index()
c = list(dd.columns)
c[-1] = 'Maximum Drawdown'
dd.columns = c
dd.sort_values(['Maximum Drawdown'], inplace=True)
dd = dd.iloc[:10]
dd = pd.merge(dd, data, on=['Ticker', 'Filing Date'], how='left')
dd.to_excel('10 worst drawdown.xlsx')
tickers = dd['Ticker'].unique()
for ticker in tickers:
    temp = dd[dd['Ticker'] == ticker]
    plt.figure(figsize=(10, 6))
    plt.plot(temp['Date'], temp['Close'], label='Close Price')
    plt.axvline(temp['Date'].iloc[10], color='red', linestyle='--', label='Filing Date')
    plt.title(f'{ticker} Stock Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend(loc='upper left')
    plt.grid(True)  # Rotate date labels
    plt.gcf().autofmt_xdate(rotation=45)  # Rotate date labels by 45 degrees
    plt.savefig(f'{ticker}.png', dpi=300)
    plt.close()
