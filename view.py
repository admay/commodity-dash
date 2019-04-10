import pandas as pd
import ffn

import config
from stats import get_index_stats, get_index_traces

def create_dash_table(index, df):
    stats = get_index_stats(index, df)
    headers = [
            {'name': 'ID', 'id': 0},
            {'name': 'header_1', 'id': 1},
            {'name': 'header_2', 'id': 2},
            {'name': 'header_3', 'id': 3},
            {'name': 'header_4', 'id': 4},
            ]
    data = [
            {'1': '1 x 1', '2': '1 x 2', '3': '1 x 3', '4': '1 x 4'},
            {'1': '2 x 1', '2': '2 x 2', '3': '2 x 3', '4': '2 x 4'},
            {'1': '3 x 1', '2': '3 x 2', '3': '3 x 3', '4': '3 x 4'},
            {'1': '4 x 1', '2': '4 x 2', '3': '4 x 3', '4': '4 x 4'}
            ]
    return [headers, data]

# maybe I should break these into multiple functions and add toggles for the users
def create_dash_graph(index, df, stats):
    """
    Creates dash compatible graph components for displaying

    Parameters
    __________
    index - Commodity index to be analyzed, will default to `headers[0]` if no index is selected
            The default value here is mostly for when the app first initializes

    Returns
    _______
    A `dcc.Graph` compatible dict for displaying data
    Currently will contain:
    - commodity price, `price_trace`
    - commodity monthly return, `monthly_return_trace`
    """
    # set a default index if none is selected
    # used for app startup
    index = index if index else default_header
    print('Selecting index: {index}'.format(index=index))

    # create trace dicts here
    traces = get_index_traces(index, df, stats)

    ret = { 'data': traces, 'layout': create_view_layout(index) }
    return ret

def create_view_layout(index):
    """
    Creates the dashboard layout

    Parameters
    __________
    index - String denoting the selected index to be used as the title

    Returns
    _______
    A dash compatible dict describing the layout
    """
    return { 'title': index, **config.AXIS_CONFIG.BASE }

