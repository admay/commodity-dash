import ffn
#%pylab inline

import pandas as pd

def get_index_stats(index, df):
    """
    Util function for getting the ffn PerformanceStats of an index from a dataframe

    Say it with me kids,
    "MO. NAD."
    """
    prices = df[[index, 'DATE']].set_index('DATE')
    return prices.calc_stats()
