# -*- coding: utf-8 -*-
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from cache import Cache
from view import create_dash_graph, create_dash_table
from sanatize import sanatize_dataframe, get_headers

# TODO: Add CSV validation for warning of bad data formats
# TODO: Add file upload for ease of use by developers

# Some Dash provided CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# boujie cache for whack memoization
dash_cache = Cache()

# upload data on startup
df = sanatize_dataframe(pd.read_csv("./data.csv"))

# grab the headers here before we add data
headers = get_headers(df)

# create the dash app
# port 8050 by default
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Commodity Data'),
    dcc.Dropdown(id='commodity-selector', options=[{'label': h, 'value': h} for h in headers]),
    dcc.Graph(id='commodity-graph'),
    dt.DataTable(id='commodity-stats')
    ])

@app.callback(
        [ Output('commodity-graph', 'figure'),
          Output('commodity-stats', 'columns'),
          Output('commodity-stats', 'data')],
        [ Input('commodity-selector', 'value') ])
def build_view(index):
    """
    Callback function to update the UI and cache resulting analysis
    """
    # get our index
    index = index if index else headers[0]

    # create our df and stats
    index_df = df[['DATE', 'YEAR', 'MONTH', index]]

    # boy do I with this was a monad
    stats_df = index_df[[index, 'DATE']].set_index('DATE')
    index_stats = stats_df.calc_stats()

    # make a graph
    graph_figure = dash_cache.get(index) if dash_cache.check(index) else create_dash_graph(index, index_df, index_stats)

    # cache the graph
    dash_cache.put(index, graph_figure)

    # create a table
    table_headers, table_data = create_dash_table(index, df)

    # cache the table
    return [ graph_figure, table_headers, table_data ]


if __name__ == '__main__':
    app.run_server(debug=True)
    # run(df, headers[0])

