import pandas as pd

# Load the data
data = pd.read_csv('8k_with_prices.csv')

# Group by Ticker and Filing Date
grouped_data = data.groupby(['Ticker', 'Filing Date', 'Date'])


# Define custom aggregation functions
def aggregate_accession_numbers(series):
    return list(series) if len(series) > 1 else series.iloc[0]


def extend_items(series):
    return ', '.join(map(str, series)) if len(series) > 1 else series.iloc[0]


# Apply the aggregation
aggregated_data = grouped_data.agg({
    'Adj Close': 'first',
    'Accession Number': aggregate_accession_numbers,
    'Beta': 'first',
    'Market': 'first',
    'Ret': 'first',
    'Items': extend_items
}).reset_index()

# Save the aggregated data to a new file
output_file_path = '8k_with_prices.csv'
aggregated_data.to_csv(output_file_path, index=False)
