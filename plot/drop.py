import pandas as pd

data = pd.read_csv('8k_with_prices.csv')
data = data[data['Ticker'] != 'CHRD']
data = data[data['Ticker'] != 'PECO']
data.to_csv('8k_with_prices.csv')
