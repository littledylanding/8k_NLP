import pandas as pd
import matplotlib.pyplot as plt


def mdd(data):
    mid = len(data) // 2
    m1 = data['Adj Close'].iloc[:mid].mean()
    m2 = data['Adj Close'].iloc[mid + 1:].mean()
    return (m2 - m1) / m1


window = 5
data = pd.read_csv('8k_with_prices.csv')
data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])
data = data[(data['Filing Date'] < pd.to_datetime('2020-02-01')) | (data['Filing Date'] > pd.to_datetime('2020-03-31'))]
dd = data.groupby(['Ticker', 'Filing Date']).apply(mdd).reset_index()
c = list(dd.columns)
c[-1] = 'Maximum Drawdown'
dd.columns = c
dd.sort_values(['Maximum Drawdown'], inplace=True)
dd = dd.iloc[:100]
data = pd.merge(dd, data, on=['Ticker', 'Filing Date'], how='left')
data.to_excel('100 worst drawdown.xlsx')
print()
for index, row in dd.iterrows():
    ticker = row['Ticker']
    fd = row['Filing Date']
    fd_str = ' ' + fd.strftime('%Y-%m-%d')

    temp = data[(data['Ticker'] == ticker) & (data['Filing Date'] == fd)]
    plt.figure(figsize=(10, 6))
    plt.plot(temp['Date'], temp['Adj Close'], label='Close Price')
    plt.axvline(temp['Date'].iloc[window], color='red', linestyle='--', label='Filing Date')
    plt.title(f'{ticker} Stock Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend(loc='upper left')
    plt.grid(True)  # Rotate date labels
    plt.gcf().autofmt_xdate(rotation=45)  # Rotate date labels by 45 degrees
    plt.savefig(f'{ticker+fd_str}.png', dpi=300)
    plt.close()
