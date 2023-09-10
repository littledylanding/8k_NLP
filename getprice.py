import yfinance as yf
import pandas as pd
import asyncio
import datetime as dt


def get_businessdays(date, window):
    start, end = None, None
    return start, end


async def process_job(job, window):
    ticker, date = job
    start_date, end_date = get_businessdays(date, window)
    end_date = (dt.strptime(end_date, '%Y-%m-%d') + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    temp_data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
    df = temp_data.reset_index()
    df.columns = ['Date', 'Close']
    df['Ticker'] = ticker
    df = df[['Date', 'Ticker', 'Close']]
    return df


# If call this function, use the command asyncio.run(get_price(tickers, dates, window))
async def get_price(tickers, dates, window):
    tasks = [asyncio.create_task(process_job(job, window)) for job in zip(tickers, dates)]
    results = await asyncio.gather(*tasks)
    data = pd.DataFrame([])
    for temp_data in results:
        data = pd.concat([data, temp_data], ignore_index=True)
    return data
