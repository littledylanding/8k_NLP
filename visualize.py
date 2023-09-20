import pandas as pd
import matplotlib.pyplot as plt


def plot_mean_ret(data, items):
    for item in items:
        temp_data = data[data['section'] == item].groupby(['company', 'fillingdate']).pct_change()



    return


data = pd.read_csv('data.csv')
