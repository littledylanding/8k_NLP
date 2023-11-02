import pandas as pd
import pandas_market_calendars as mcal
from datetime import timedelta
from xbbg import blp
from concurrent.futures import ThreadPoolExecutor
import asyncio


def get_businessdays(target_date, k, exchange='NYSE'):
    calendar = mcal.get_calendar(exchange)
    target_date = pd.Timestamp(target_date)
    start_date = target_date - pd.Timedelta(days=max(365, 2 * k))
    end_date = target_date + pd.Timedelta(days=max(365, 2 * k))
    schedule = calendar.schedule(start_date=start_date, end_date=end_date)
    idx = schedule.index.get_loc(target_date, method='nearest')
    nearby_dates = schedule.iloc[idx - k:idx + k + 1].index.tolist()
    return min(nearby_dates), max(nearby_dates)


async def process_equity(equity_data, window):
    ticker, filing_dates = equity_data
    filing_dates = sorted(filing_dates)
    start_date, _ = get_businessdays(filing_dates[0], window)
    _, end_date = get_businessdays(filing_dates[-1], window)
    end_date = (end_date + timedelta(days=1)).strftime('%Y-%m-%d')
    bloomberg_ticker = f'{ticker} US Equity'
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        temp_data = await loop.run_in_executor(
            executor,
            blp.bdh,
            bloomberg_ticker,
            ['Px_Last'],
            start_date.strftime('%Y-%m-%d'),
            end_date
        )
    temp_data = temp_data.droplevel(0, axis=1).reset_index()
    temp_data.columns = ['Date', 'Close']
    temp_data['Ticker'] = ticker
    for filing_date in filing_dates:
        temp_data[f'Filing Date {filing_date}'] = filing_date
    return temp_data


async def get_price(tickers, dates, window):
    equity_data = [(ticker, dates[tickers == ticker]) for ticker in set(tickers)]
    tasks = [asyncio.create_task(process_equity(data, window)) for data in equity_data]
    results = await asyncio.gather(*tasks)
    data = pd.DataFrame([])
    for temp_data in results:
        data = pd.concat([data, temp_data], ignore_index=True)
    return data


# Reading the original 8K information Excel file
eight_k_df = pd.read_excel('FilingData.xlsx')
eight_k_df.drop_duplicates(inplace=True)
eight_k_df['Filing Date'] = pd.to_datetime(eight_k_df['Filing Date'])
tickers = eight_k_df['Ticker'].values
dates = eight_k_df['Filing Date'].values
window = 10
result_df = asyncio.run(get_price(tickers, dates, window))

# Saving the data to a new CSV file
result_df.to_csv('8k_with_prices.csv', index=False)
