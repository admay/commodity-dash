# -*- coding: utf-8 -*-
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import optparse

from cache import Cache
from view import create_dash_graph, create_dash_table
from sanatize import sanatize_dataframe, get_headers
from stats import get_index_stats

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
    dcc.Dropdown(
        id='commodity-selector',
        options=[{'label': h, 'value': h} for h in headers]
        ),
    dcc.Graph(id='commodity-graph'),
    dt.DataTable(
        id='commodity-stats',
        style_table={
            'overflowX': 'scroll',
            'maxWidth': '100%',
            },
        )
    ])


@app.callback(
        [Output('commodity-graph', 'figure'),
         Output('commodity-stats', 'columns'),
         Output('commodity-stats', 'data')],
        [Input('commodity-selector', 'value')])
def build_view(index):
    """
    Callback function to update the UI and cache resulting analysis
    """
    # get our index
    index = index if index else headers[0]

    # create our df and stats
    index_df = df[['DATE', 'YEAR', 'MONTH', index]]
    stats_df = get_index_stats(index, index_df)

    # make a graph
    graph_figure = (
            dash_cache.get(index)
            if dash_cache.check(index)
            else create_dash_graph(index, index_df, stats_df)
            )

    # cache the graph
    dash_cache.put(index, graph_figure)

    # create a table
    table_headers, table_data = create_dash_table(index, df)

    # cache the table
    return [graph_figure, table_headers, table_data]


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option(
            '-d', '--debug', action='store',
            dest='DEBUG', help='run server in debug mode',
            default='dev')
    options, args = parser.parse_args()

    print(options)

    app.run_server(debug=options.DEBUG.lower() == 'true')
