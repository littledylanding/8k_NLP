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
                slice_indices = slice(None, 5)
                x_values = x[:mid]
            else:
                slice_indices = slice(4, None)
                x_values = x[mid - 1:]
            cum_ret = (group.iloc[slice_indices]['Ret'][1:len(x_values)] + 1).cumprod() - 1
            plt.plot(x_values, [0] + list(np.squeeze(cum_ret.values)),linestyle='-', linewidth=1.5, color=color)
    plt.axvline(x=4, color='c', label='Day before Fling Date')
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Return', fontsize=14)
    plt.title(f'Cumulative Return', fontsize=16)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig('normal')
    plt.close()


# Example usage
data = pd.read_excel('100 flat filings.xlsx')
data.drop_duplicates(inplace=True)
data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])

plot_mean_cum_ret(data)
