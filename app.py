# -*- coding: utf-8 -*-
import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import ffn

# TODO: Move this all into a startup script
# TODO: Add CSV validation for warning of bad data formats
# TODO: Add file upload for ease of use by developers

# Some Dash provided CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# boujie cache for whack memoization
dash_cache = {}

# upload data on startup
# can be optimized for runtime using real persistence
# optimizing for runtime now to reduce I/O costs
df = pd.read_csv("./data.csv")

# make all cols uppercase for consistency
df.columns = df.columns.map(lambda col: col.upper())

# grab the headers here before we add data
headers = list(df)
# date isn't a commodity so we're going to drop it by label here
headers.remove('DATE')

# use real datetimes in the dataframe
df['DATE'] = pd.to_datetime(df['DATE'])
# add date breakup cols for grouping and axis labeling later
df['YEAR'], df['MONTH'], df['DAY'] = df['DATE'].dt.year, df['DATE'].dt.month, df['DATE'].dt.day

# and create a date series for the x-axis
date_series = df['DATE']
som_series = pd.date_range(date_series.iloc[0], date_series.iloc[-1], freq='M').map(lambda d: d.replace(day=1))

# create the dash app
# port 8050 by default
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Commodity Data'),
    # generate_table(df)
    dcc.Dropdown(id='commodity-selector', options=[{'label': h, 'value': h} for h in headers]),
    dcc.Graph(id='commodity-graph')
    ])

trace_opts = {
            'monthly_return': {
                'name': 'Monthly Return',
                'type': 'bar',
                'yaxis': 'y4',
                'side': 'left',
                'position': 0.3
            },
            'volatility': {
                'name': 'Volatility',
                'type': 'line',
                'yaxis': 'y3',
                'side': 'right',
                'position': 0.45
            },
            'drawdown': {
                'name': 'Drawdown',
                'type': 'line',
                'yaxis': 'y2',
            },
            'price': {
                'name': 'Price',
                'type': 'line',
                'yaxis': 'y1',
                'side': 'left',
                'position': 0.15
            }
        }

def cache_components(key, data):
    """
    Caches a give data object in the `dash_cache`

    Parameters
    __________
    key - Cache key for lookup
    data - Data being stored

    Returns
    _______
    0 on success, 1 on failure
    """
    dash_cache[key]=data
    return 0

# maybe I should break these into multiple functions and add toggles for the users
def create_dash_components(index):
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
    index = index if index else headers[0]
    print('Selecting index: {index}'.format(index=index))

    # split index data from base df
    df_index = df[['DATE', 'YEAR', 'MONTH', index]]

    monthly_return_data = df_index.groupby(['YEAR', 'MONTH']).apply(lambda p: p.iloc[-1] - p.iloc[0])

    # create trace dicts here
    price_trace = create_trace(
            x_data=date_series,
            y_data=df_index[index],
            opts=trace_opts['price']
            )

    drawdown_trace = create_trace(
            x_data=date_series,
            y_data=df_index[index].to_drawdown_series(),
            opts=trace_opts['drawdown']
            )

    volatility_trace = create_trace(
            x_data=date_series,
            y_data=df_index[index].rolling(3).std(),
            opts=trace_opts['volatility']
            )

    monthly_return_trace = create_trace(
            x_data=som_series,
            y_data=monthly_return_data[index],
            opts=trace_opts['monthly_return']
            )

    ret = {
        'data':[
            price_trace,
            drawdown_trace,
            volatility_trace,
            monthly_return_trace
            ],
        'layout': create_view_layout(index)
        }
    return ret

def create_trace(x_data, y_data, opts):
    return {
            'y': y_data,
            'x': x_data,
            **opts
            }

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
    return {
            'title': index,
            'xaxis': {
                'domain': [0.1, 0.9]
                },
            'yaxis': {
                'title': 'Price'
                },
            'yaxis2': {
                'title': 'Drawdown' ,
                'overlaying': 'y',
                'side': 'left',
                'position': 0.05
                },
            'yaxis3': {
                'title': 'Volatility',
                'overlaying': 'y',
                'side': 'right'
                },
            'yaxis4': {
                'title': 'Monthly Return',
                'overlaying': 'y',
                'side': 'right',
                'position': 0.95
                }
            }

@app.callback(
        Output('commodity-graph', 'figure'),
        [Input('commodity-selector', 'value')])
def build_view(index):
    """
    Callback function to update the UI and cache resulting analysis
    """
    components = dash_cache[index] if index in dash_cache else create_dash_components(index)
    cache_success = cache_components(index, components)
    if (cache_success != 0): print("There was an error cacheing the index components for {index}".format(index=index))
    return components


if __name__ == '__main__':
    app.run_server(debug=True)
