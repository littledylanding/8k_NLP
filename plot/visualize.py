import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

cwd = os.getcwd()


def plot_mean_cum_ret(data, items, up=0.75, down=0.25):
    for item in items:
        pct_changes = data[data['Items'] == item].groupby(['Ticker', 'Filing Date'])[['Ticker', 'Filing Date', 'Ret', 'Date']].apply(lambda x: x.iloc[9:]).drop_duplicates()
        median = [0]
        upper = [0]
        lower = [0]
        max_len = max(pct_changes.groupby(level=[0, 1]).apply(len))
        mid = max_len // 2 - 1
        x = np.array(range(mid + 2))
        mean = [0]
        for i in range(mid+1, max_len):
            nth_values = pct_changes.apply(
                lambda group: group.cumsum().iloc[i] if len(group) > i else np.nan)
            median.append(nth_values.median())
            upper.append(nth_values.quantile(q=up, interpolation='nearest'))
            lower.append(nth_values.quantile(q=down, interpolation='nearest'))
            mean.append(nth_values.mean())

        plt.plot(x, median, label='Median Cumulative Return', linestyle='-', linewidth=1.5)
        plt.plot(x, upper, label='{q} Quantile Cumulative Return'.format(q=int(up * 100)), linestyle='-', linewidth=1.5)
        plt.plot(x, lower, label='{q} Quantile Cumulative Return'.format(q=int(down * 100)), linestyle='-',
                 linewidth=1.5)
        plt.plot(x, mean, label='Mean Cumulative Return', linestyle='-', linewidth=1.5)
        plt.xticks(x, x)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Return', fontsize=14)
        plt.title('Cumulative Return of Item {}'.format(item), fontsize=16)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig('{}.jpg'.format(cwd + '/figures/' + item))
        plt.close()
    return


data = pd.read_csv('8k_with_prices.csv')
data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])
grouped = data.groupby(['Ticker', 'Filing Date']).apply(lambda x: max(x['Items'].apply(lambda x: len(x))))

data = data.assign(Items=data['Items'].str.split(',')).explode('Items', ignore_index=True)
data.drop_duplicates(inplace=True)

items = data['Items'].unique()
items = [item for item in items if not isinstance(item, float) or not np.isnan(item)]
plot_mean_cum_ret(data, items)
