import pandas as pd


def mdd(data):
    Roll_Max = data['Close'].cummax()
    Daily_Drawdown = data['Close'] / Roll_Max - 1
    return Daily_Drawdown.min()


data = pd.read_csv('8k_with_prices.csv')
data = data.assign(Section=data['Section'].str.split(',')).explode('Section', ignore_index=True)

data.drop_duplicates(inplace=True)
data.dropna(subset=['Close'], inplace=True)

data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])

data = data.groupby(['Ticker', 'Filing Date', 'Section']).apply(mdd).reset_index()
data.rename({0:'Maximum Drawdown'}, inplace=True)
