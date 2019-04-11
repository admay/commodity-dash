import pandas as pd
import ffn

import config


def get_index_stats(index, df):
    """
    Util function for getting the ffn PerformanceStats of an
    index from a dataframe

    Say it with me kids,
    "MO. NAD."
    """
    prices = df[[index, 'DATE']].set_index('DATE')
    return prices.calc_stats()


def create_trace(x_data, y_data, opts={}):
    """
    Helper function to create trace dicts

    Parameters
    __________
    x_data - Series repreenting the x axis
    y_data - Series representing the y axis
    opts - Dict of options containing any and all extra,
           trace specific configuration
    """
    return {'y': y_data, 'x': x_data, **opts}


def get_index_traces(index, df, stats):
    # Create our default time series'
    date_series = df['DATE']

    price_trace = create_trace(date_series, df[index], config.TRACE_OPTS.PRICE)

    drawdown_trace = create_trace(
            date_series,
            df[index].to_drawdown_series(),
            config.TRACE_OPTS.DRAWDOWN
            )

    volatility_trace = create_trace(
            date_series,
            df[index].rolling(3).std(),
            config.TRACE_OPTS.VOLATILITY
            )

    mr_series = pd.Series(stats[index].monthly_returns)
    monthly_return_trace = create_trace(
            mr_series.index,
            mr_series.values,
            config.TRACE_OPTS.MONTHLY_RETURN
            )

    traces = [
            price_trace,
            drawdown_trace,
            volatility_trace,
            monthly_return_trace
            ]
    return traces
