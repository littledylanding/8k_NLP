import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import itertools


def plot_mean_cum_ret(data):
    data.sort_values(['Ticker', 'Filing Date', 'Date'])
    grouped_data = data.groupby(['Ticker', 'Filing Date'])
    colors = itertools.cycle(['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black'])

    for (ticker, filing_date), group in grouped_data:
        color = next(colors)  # Get the next color from the cycle
        group = group.reset_index(drop=True)
        mid = group[group['Date'] == filing_date].index[0]
        x = np.array(range(len(group)))
        for part in [0, 1]:
            if part == 0:
                slice_indices = slice(None, 6)
                x_values = x[:mid+1]
                cum_ret = (group.iloc[slice_indices]['Adj Close'] - group.iloc[slice_indices]['Adj Close'].iloc[-1]) / group.iloc[slice_indices]['Adj Close'].iloc[-1]
            else:
                slice_indices = slice(5, None)
                x_values = x[mid:]
                cum_ret = (group.iloc[slice_indices]['Adj Close'] - group.iloc[slice_indices]['Adj Close'].iloc[0]) / group.iloc[slice_indices]['Adj Close'].iloc[0]
            plt.plot(x_values, list(np.squeeze(cum_ret.values)),linestyle='-', linewidth=1.5, color=color)
    plt.axvline(x=5, color='c', label='Filing Date')
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Return', fontsize=14)
    plt.title(f'Cumulative Return', fontsize=16)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig('worst')
    plt.close()


# Example usage
data = pd.read_excel('100 worst drawdown.xlsx')
data.drop_duplicates(inplace=True)
data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])

plot_mean_cum_ret(data)
