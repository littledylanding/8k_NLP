import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

cwd = os.getcwd()


def plot_mean_cum_ret(data, items, up=0.75, down=0.25):
    data.sort_values(['Ticker', 'Filing Date', 'Date'])
    for item in items:
        print(item)
        grouped_data = data[data['Items'] == item].groupby(['Accession Number'])[['Ret']]

        max_len = max(grouped_data.apply(len))
        mid = max_len // 2
        x = np.array(range(max_len))

        for part in [0, 1]:
            if part == 0:
                slice_indices = slice(None, 9)
                x_values = x[:mid]
            else:
                slice_indices = slice(9, None)
                x_values = x[mid-1:]

            median = [0]
            upper = [0]
            lower = [0]
            mean = [0]

            for i in range(1, len(x_values)):
                nth_values = grouped_data.apply(
                    lambda group: (group.iloc[slice_indices][1:i + 1] + 1).prod() - 1
                )
                median.append(nth_values['Ret'].median())
                upper.append(nth_values['Ret'].quantile(q=up, interpolation='nearest'))
                lower.append(nth_values['Ret'].quantile(q=down, interpolation='nearest'))
                mean.append(nth_values['Ret'].mean())

            plt.plot(x_values, median, label='Median Cumulative Return' if part == 0 else "", linestyle='-',
                     linewidth=1.5, color='b')
            plt.plot(x_values, upper, label=f'{int(up * 100)} Quantile Cumulative Return' if part == 0 else "",
                     linestyle='-', linewidth=1.5, color='g')
            plt.plot(x_values, lower, label=f'{int(down * 100)} Quantile Cumulative Return' if part == 0 else "",
                     linestyle='-', linewidth=1.5, color='r')
            plt.plot(x_values, mean, label='Mean Cumulative Return' if part == 0 else "", linestyle='-', linewidth=1.5, color='k')
        plt.axvline(x=9, color='c', label='Day before Fling Date')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xlabel('Time', fontsize=14)
        plt.ylabel('Return', fontsize=14)
        plt.title(f'Cumulative Return of Item {item}', fontsize=16)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(f'{cwd}/figures/{item}.jpg')
        plt.close()
    return


window = 10
data = pd.read_pickle('df_item_sp600_daily_return_1106.pkl')
data = data.assign(Items=data['Items'].str.split(', ')).explode('Items', ignore_index=True)

data.drop_duplicates(inplace=True)
data.dropna(subset=['Adj Close'], inplace=True)
data = data.groupby(['Items', 'Accession Number']).filter(lambda x: len(x) == 2 * window + 1).reset_index(
    drop=True)
data['Filing Date'] = pd.to_datetime(data['Filing Date'])
data['Date'] = pd.to_datetime(data['Date'])

items = data['Items'].unique()
items = sorted([item for item in items if not isinstance(item, float) or not np.isnan(item)])
err = ['2.02101', '2.02104', '7.01104']
for x in err:
    if x in items:
        items.remove(x)
plot_mean_cum_ret(data, items)
