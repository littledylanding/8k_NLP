import pandas as pd
import numpy as np


def mdd(data):
    mid = len(data) // 2
    Roll_Max = data['Close'].iloc[mid - 2:mid + 3].cummax()
    Daily_Drawdown = data['Close'].iloc[mid - 2:mid + 3] / Roll_Max - 1
    return Daily_Drawdown.min()


# Define the function for mean difference calculation
def mdd2(data):
    mid = len(data) // 2
    m1 = data['Adj Close'].iloc[:mid].mean()
    m2 = data['Adj Close'].iloc[mid + 1:].mean()
    return (m2 - m1) / m1


# Load the data from a CSV file
data = pd.read_csv('8k_with_prices.csv')
data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])

# Group by 'Accession Number', apply the mdd2 function, and get the 100 lowest results
grouped_data = data.groupby('Accession Number').apply(mdd2).reset_index()
grouped_data.columns = ['Accession Number', 'MDD2']
lowest_100 = grouped_data.nsmallest(100, 'MDD2')

# Display the result
print(lowest_100)
