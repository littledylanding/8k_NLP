import yfinance as yf
import pandas as pd
import asyncio
from datetime import datetime as dt, timedelta
import pandas_market_calendars as mcal


def get_businessdays(target_date, k, exchange='NYSE'):
    calendar = mcal.get_calendar(exchange)

    target_date = pd.Timestamp(target_date)

    start_date = target_date - pd.Timedelta(days=max(365, 2*k))  # 1 year before
    end_date = target_date + pd.Timedelta(days=max(365, 2*k))  # 1 year after
    schedule = calendar.schedule(start_date=start_date, end_date=end_date)

    idx = schedule.index.get_loc(target_date, method='nearest')

    nearby_dates = schedule.iloc[idx - k:idx + k + 1].index.tolist()

    return min(nearby_dates), max(nearby_dates)


async def process_job(job, window):
    ticker, date = job
    start_date, end_date = get_businessdays(date, window)
    end_date = (end_date + timedelta(days=1)).strftime('%Y-%m-%d')
    temp_data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
    df = temp_data.reset_index()
    df.columns = ['Date', 'Close']
    df['Ticker'] = ticker
    df = df[['Date', 'Ticker', 'Close']]
    df['Report Date'] = date
    return df


# If call this function, use the command asyncio.run(get_price(tickers, dates, window))
async def get_price(tickers, dates, window):
    tasks = [asyncio.create_task(process_job(job, window)) for job in zip(tickers, dates)]
    results = await asyncio.gather(*tasks)
    data = pd.DataFrame([])
    for temp_data in results:
        data = pd.concat([data, temp_data], ignore_index=True)
    return data

'''
tickers = ['MSFT', 'AAPL']
dates = ['2023-08-13', '2022-07-18']
window = 10
print(asyncio.run(get_price(tickers, dates, window)))
'''
