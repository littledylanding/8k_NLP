import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_mean_ret(data, items):
    for item in items:
        temp_data = data[data['section'] == item].groupby(['company', 'fillingdate'])['close']
        pct_changes = temp_data.apply(lambda x: x.pct_change().dropna())
        means = []
        max_len = max(pct_changes.groupby(level=[0, 1]).apply(len))
        mid = max_len // 2
        x = np.array(range(2, max_len + 2)) - mid
        for i in range(max_len):
            nth_values = pct_changes.groupby(level=[0, 1]).apply(lambda x: x.iloc[i] if i < len(x) else np.nan)
            means.append(nth_values.mean())

        plt.plot(x, means, label='Mean Daily Return', linestyle='-', linewidth=1.5)
        plt.axvline(mid, color='grey', linestyle='--', linewidth=0.5)  # Vertical line at middle x-point
        plt.scatter(mid, means[mid], color='red')  # Mark the middle x-point in red

        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Mean Percentage Change', fontsize=14)
        plt.title('Mean of Daily Return of item {}'.format(item), fontsize=16)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig('{}.jpg'.format(item))
        plt.close()
    return


data = pd.read_csv('data.csv')
data['section'] = data['section'].str.split(',')
data = data.explode('section', ignore_index=True)
items = []
plot_mean_ret(data, items)
