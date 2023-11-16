import pandas as pd

data = pd.read_excel('100 flat filings.xlsx')
data = data.drop_duplicates(subset=['Ticker', 'Filing Date'])
print(len(data))
