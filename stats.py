import ffn
#%pylab inline

import pandas as pd

def get_index_stats(index, df):
    prices = df[[index, 'DATE']].set_index('DATE')
    # print(prices.calc_stats()[index].monthly_returns)
    return prices.calc_stats()
