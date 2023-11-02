import yfinance as yf
import pandas as pd
import asyncio
from datetime import timedelta
import pandas_market_calendars as mcal
import numpy as np


def get_businessdays(target_date, k, exchange='NYSE'):
    calendar = mcal.get_calendar(exchange)
    target_date = pd.Timestamp(target_date)
    start_date = target_date - pd.Timedelta(days=max(365, 2 * k))
    end_date = target_date + pd.Timedelta(days=max(365, 2 * k))
    schedule = calendar.schedule(start_date=start_date, end_date=end_date)
    idx = schedule.index.get_indexer([target_date], method='nearest')[0]
    nearby_dates = schedule.iloc[idx - k:idx + k + 1].index.tolist()
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
eight_k_df = pd.read_csv('FilingData.csv')
eight_k_df['Filing Date'] = pd.to_datetime(eight_k_df['Filing Date']).dt.date
eight_k_df['Items'] = eight_k_df['Items'].str.replace('Item ', '')
eight_k_df['Items'] = eight_k_df['Items'].str.replace(' ', '')
eight_k_df = eight_k_df.groupby(['Ticker', 'Filing Date']).agg({'Items': lambda x: ','.join(x)}).reset_index()
tickers = np.squeeze(eight_k_df['Ticker'].values)
dates = np.squeeze(eight_k_df['Filing Date'].values)
window = 10
result_df = asyncio.run(get_price(tickers, dates, window))
result_df.dropna(subset=['Close'], inplace=True)
result_df['Date'] = result_df['Date'].dt.date
result_df = result_df.groupby(['Ticker', 'Filing Date']).filter(lambda x: len(x) >= 2 * window + 1).reset_index(
    drop=True)
result_df = result_df.sort_values(['Ticker', 'Filing Date', 'Date'])
start = min(result_df['Date']) - timedelta(1)
end = max(result_df['Date']) + timedelta(1)
market = yf.download('^GSPC', start=start, end=end, progress=False)['Adj Close']
market = market.reset_index()
market.columns = ['Date', 'Market']
market['Date'] = market['Date'].dt.date
market['Market'] = market['Market'].pct_change()
result_df = pd.merge(result_df, market, on='Date', how='left', suffixes=('', '_right'))
result_df['Ret'] = result_df['Close'].pct_change()
result_df['Ret'] = result_df['Ret'] - result_df['Market']
result_df = pd.merge(result_df, eight_k_df, on=['Ticker', 'Filing Date'], how='left', suffixes=('', '_right'))
result_df.to_csv('8k_with_prices.csv', index=False)
