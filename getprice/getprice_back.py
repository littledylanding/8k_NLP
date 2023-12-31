import yfinance as yf
import pandas as pd
import asyncio
from datetime import datetime as dt, timedelta
import pandas_market_calendars as mcal


def get_businessdays(target_date, k, exchange='NYSE'):
    calendar = mcal.get_calendar(exchange)
    target_date = pd.Timestamp(target_date)
    start_date = target_date - pd.Timedelta(days=max(365, 2*k))
    end_date = target_date + pd.Timedelta(days=max(365, 2*k))
    schedule = calendar.schedule(start_date=start_date, end_date=end_date)
    idx = schedule.index.get_loc(target_date, method='nearest')
    nearby_dates = schedule.iloc[idx - 1:idx+k].index.tolist()
    return min(nearby_dates), max(nearby_dates)


async def process_job(job, window):
    ticker, date = job
    start_date, end_date = get_businessdays(date, window)
    end_date = (end_date + timedelta(days=1)).strftime('%Y-%m-%d')
    temp_data = yf.download(ticker, start=start_date, end=end_date, progress=False)['Adj Close']
    df = temp_data.reset_index()
    df.columns = ['Date', 'Close']
    df['Ticker'] = ticker
    df = df[['Date', 'Ticker', 'Close']]
    df['Filing Date'] = date
    return df


# If call this function, use the command asyncio.run(get_price(tickers, dates, window))
async def get_price(tickers, dates, window):
    tasks = [asyncio.create_task(process_job(job, window)) for job in zip(tickers, dates)]
    results = await asyncio.gather(*tasks)
    data = pd.DataFrame([])
    for temp_data in results:
        data = pd.concat([data, temp_data], ignore_index=True)
    return data

# Read the original 8K information Excel file
eight_k_df = pd.read_excel('FilingData.xlsx')
eight_k_df.drop_duplicates(inplace=True)
eight_k_df['Filing Date'] = pd.to_datetime(eight_k_df['Filing Date'])
eight_k_df['Section'] = eight_k_df['Section'].str.replace('Item ', '')
eight_k_df['Section'] = eight_k_df['Section'].str.replace(' ', '')
tickers = eight_k_df['Ticker'].values
dates = eight_k_df['Filing Date'].values
window = 20
result_df = asyncio.run(get_price(tickers, dates, window))

# Merge the 8K information and stock price data into a new Excel file
merged_df = pd.merge(eight_k_df, result_df, on=['Ticker', 'Filing Date'], how='left')
merged_df.dropna(subset=['Close'], inplace=True)
merged_df['Filing Date'] = merged_df['Filing Date'].dt.date
merged_df['Date'] = merged_df['Date'].dt.date
merged_df = merged_df.groupby(['Ticker', 'Filing Date', 'Section']).filter(lambda x: len(x) >= 21).reset_index(drop=True)
# Save the integrated data to a new Excel file
merged_df.to_csv('8k_with_prices_20days_back.csv', index=False)
