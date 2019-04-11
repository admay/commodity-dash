import config
from stats import get_index_stats, get_index_traces


def create_headers(stats):
    """Creates a list of header dicts for use with dcc Tables
    """
    return [
            {'name': l[1], 'id': l[0]}
            for l in stats._stats() if l[1] is not None
            ]


def create_values(values):
    """
    Creates a list of value dicts for use with dcc Tables

    Parameters
    __________
    pd.PerformanceStats object

    Returns
    _______
    A list of one row for the table
    """
    header_list = [{v[0]: v[1]} for v in values.iteritems()]
    return [dict(pair for d in header_list for pair in d.items())]


def create_dash_table(index, df):
    stats = get_index_stats(index, df)[index]
    headers = create_headers(stats)
    values = create_values(stats.stats)
    return [headers, values]


def create_dash_graph(index, df, stats):
    """
    Creates dash compatible graph components for displaying

    Parameters
    __________
    index - Commodity index to be analyzed, will default to `headers[0]`
            If no index is selected
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
    print('Selecting index: {index}'.format(index=index))

    # create trace dicts here
    traces = get_index_traces(index, df, stats)

    ret = {'data': traces, 'layout': create_view_layout(index)}
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
    return {'title': index, **config.AXIS_CONFIG.BASE}
