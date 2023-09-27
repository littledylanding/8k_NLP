import pandas as pd


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
    items = [x for x in list(df.columns) if 'Item' in x ]
    for company_col in df['Ticker'].unique().values:
        for item_col in items:
            new_feature_col = f"{item_col}_within_{k}_bdays"
            df[new_feature_col] = 0

            for _, row in df.iterrows():
                company = row[company_col]
                target_date = row[date_col]
                start_date, end_date = get_businessdays(target_date, k)

                # Check if the item was filed within k business days for the same company
                condition = (df[company_col] == company) & (df[date_col] >= start_date) & (df[date_col] <= end_date) & (
                            df[item_col] == 1)
                if df[condition].shape[0] > 0:
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


