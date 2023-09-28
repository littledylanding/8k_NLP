import pandas as pd
import pandas_market_calendars as mcal
import seaborn as sns
import matplotlib.pyplot as plt


def get_businessdays(target_date, k, exchange='NYSE'):
    calendar = mcal.get_calendar(exchange)
    target_date = pd.Timestamp(target_date)
    start_date = target_date - pd.Timedelta(days=max(365, 2 * k))
    end_date = target_date + pd.Timedelta(days=max(365, 2 * k))
    schedule = calendar.schedule(start_date=start_date, end_date=end_date)
    idx = schedule.index.get_loc(target_date, method='nearest')
    nearby_dates = schedule.iloc[idx - k:idx + k + 1].index.tolist()
    return min(nearby_dates), max(nearby_dates)


def mark_rows_within_k_bdays(df, k):
    items = [x for x in list(df.columns) if 'Item' in x]
    for item_col in items:
        print(item_col)
        new_feature_col = f"{item_col}_within_{k}_bdays"
        df[new_feature_col] = 0
        for _, row in df.iterrows():
            company = row['Ticker']
            target_date = row['Filing Date']
            start_date, end_date = get_businessdays(target_date, k)
            condition = (df['Ticker'] == company) & (df['Filing Date'] >= start_date) & (df['Filing Date'] <= end_date) & (
                        df[item_col] == 1)
            if sum(condition) > 0:
                df.at[_, new_feature_col] = 1
    return df


eight_k_df = pd.read_excel('FilingData.xlsx')
eight_k_df['Filing Date'] = pd.to_datetime(eight_k_df['Filing Date'])
eight_k_df['Items List'] = eight_k_df['Section'].str.split(', ')
items_dummies = pd.get_dummies(eight_k_df['Items List'].apply(pd.Series).stack()).sum(level=0)
data_cleaned = pd.concat([eight_k_df, items_dummies], axis=1)
data_cleaned['Filing Date'] = pd.to_datetime(data_cleaned['Filing Date'])
data_cleaned.drop(['Section', 'Items List'], axis=1, inplace=True)
data_cleaned.sort_values(by=['Ticker', 'Filing Date'], inplace=True)
data = mark_rows_within_k_bdays(data_cleaned, 20)

item_cols = [col for col in data.columns if 'Item' in col and '_within_20_bdays' not in col]
lagged_cols = [f"{col}_within_20_bdays" for col in item_cols]

corr_matrix = data[item_cols + lagged_cols].corr().loc[item_cols, lagged_cols]

plt.figure(figsize=(15, 12))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, linecolor='white')
plt.title("Correlation Heatmap of Items vs. Their Lagged Versions")
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()