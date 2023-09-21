import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_mean_ret(data, items):
    for item in items:
        temp_data = data[data['Section'] == item].groupby(['Ticker', 'Filing Date'])['Close']
        pct_changes = temp_data.apply(lambda x: x.pct_change().dropna())
        means = []
        max_len = max(pct_changes.groupby(level=[0, 1]).apply(len))
        mid = max_len // 2
        x = np.array(range(2, max_len + 2)) - mid
        for i in range(max_len):
            nth_values = pct_changes.groupby(level=[0, 1]).apply(lambda x: x.iloc[i] if i < len(x) else np.nan)
            means.append(nth_values.mean())

        plt.plot(x, means, label='Mean Daily Return', linestyle='-', linewidth=1.5)
        plt.axvline(0, color='grey', linestyle='--', linewidth=0.5)  # Vertical line at middle x-point
        plt.scatter(0, means[mid-2], color='red')  # Mark the middle x-point in red
        plt.xticks(x, x)
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Return', fontsize=14)
        plt.title('Mean of Daily Return of Item {}'.format(item), fontsize=16)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig('{}.jpg'.format(item))
        plt.close()
    return


data = pd.read_csv('8k_with_prices.csv')
data = data.assign(Section=data['Section'].str.split(',')).explode('Section', ignore_index=True)

data.drop_duplicates(inplace=True)
data.dropna(subset=['Close'], inplace=True)

data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])

grouped = data.groupby(['Ticker', 'Filing Date', 'Section'])
data = grouped.filter(lambda x: len(x) >= 21).reset_index(drop=True)

items = data['Section'].unique()
items = [item for item in items if not isinstance(item, float) or not np.isnan(item)]
plot_mean_ret(data, items)
