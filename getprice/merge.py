import pandas as pd

price = pd.read_csv('8k_with_prices_neutral.csv')
price['Filing Date'] = pd.to_datetime(price['Filing Date'])
items = pd.read_csv('FilingData.csv')
items['Filing Date'] = pd.to_datetime(items['Filing Date'])
data = pd.merge(price, items, on=['Ticker', 'Filing Date'], how='left', suffixes=('', '_right'))
data['Filing Date'] = data['Filing Date'].dt.date
data['Items'] = data['Items'].str.replace(' ', '')
data.to_csv('8k_with_prices.csv')
