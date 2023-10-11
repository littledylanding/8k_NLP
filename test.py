# Reload the data
data = pd.read_excel("FilingData.xlsx")

# Split the 'Items Filed' column into a list of items
data['Items List'] = data['Items Filed'].str.split(', ')

# Create a binary matrix for each item
items_dummies = pd.get_dummies(data['Items List'].apply(pd.Series).stack()).sum(level=0)

# Merge the binary matrix with the original dataframe
data_cleaned = pd.concat([data, items_dummies], axis=1)

# Convert the 'Date' column to a datetime format
data_cleaned['Date'] = pd.to_datetime(data_cleaned['Date'])

# Drop the 'Items Filed' and 'Items List' columns as they are no longer needed
data_cleaned.drop(['Items Filed', 'Items List'], axis=1, inplace=True)

# Sort the data by Company and Date for lag analysis
data_cleaned.sort_values(by=['Company', 'Date'], inplace=True)

# Display the first few rows of the cleaned data
data_cleaned.head()