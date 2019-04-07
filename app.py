# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from cache import Cache
from view import create_dash_components

# TODO: Add CSV validation for warning of bad data formats
# TODO: Add file upload for ease of use by developers

# Some Dash provided CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# boujie cache for whack memoization
dash_cache = Cache()

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

@app.callback(
        Output('commodity-graph', 'figure'),
        [Input('commodity-selector', 'value')])
def build_view(index):
    """
    Callback function to update the UI and cache resulting analysis
    """
    components = dash_cache.get(index) if dash_cache.check(index) else create_dash_components(index, df, date_series, som_series, headers[0])
    cache_success = dash_cache.put(index, components)
    if (cache_success == False): print("There was an error cacheing the index components for {index}".format(index=index))
    return components


if __name__ == '__main__':
    app.run_server(debug=True)
