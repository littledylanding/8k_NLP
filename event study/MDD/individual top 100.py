import pandas as pd
import matplotlib.pyplot as plt


def calculate_std_diff(data):
    mid = len(data) // 2 - 1
    std_before = data['Adj Close'].iloc[:mid].std()
    std_after = data['Adj Close'].iloc[mid + 1:].std()
    return std_before - std_after


def mdd(data):
    mid = len(data) // 2
    Roll_Max = data['Adj Close'].iloc[mid - 2:mid + 3].cummax()
    Daily_Drawdown = data['Adj Close'].iloc[mid - 2:mid + 3] / Roll_Max - 1
    return Daily_Drawdown.min()


window = 5
data = pd.read_csv('8k_with_prices.csv')
data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])
data = data[(data['Filing Date'] < pd.to_datetime('2020-02-01')) | (data['Filing Date'] > pd.to_datetime('2020-03-31'))]

# Calculate std before and after the filing date and reset index
std_diffs = data.groupby(['Ticker', 'Filing Date']).apply(calculate_std_diff).reset_index()
std_diffs.rename(columns={0: 'std_diff'}, inplace=True)

# Merge std_diffs back to the data
data = pd.merge(data, std_diffs, on=['Ticker', 'Filing Date'])
data = data[data['std_diff'] < 0]  # Filter based on std condition

# Calculate maximum drawdown
dd = data.groupby(['Ticker', 'Filing Date']).apply(mdd).reset_index()
c = list(dd.columns)
c[-1] = 'Maximum Drawdown'
dd.columns = c
dd.sort_values(['Maximum Drawdown'], inplace=True)
dd = dd.iloc[:100]
data = pd.merge(dd, data, on=['Ticker', 'Filing Date'], how='left')
data.to_excel('100 worst drawdown.xlsx')

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
    plt.grid(True)
    plt.gcf().autofmt_xdate(rotation=45)
    plt.savefig(f'worst\\{ticker + fd_str}.png', dpi=300)
    plt.close()
