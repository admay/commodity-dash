# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

import datetime as dt

# Some Dash provided CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
start_of_month_series = pd.date_range(date_series.iloc[0], date_series.iloc[-1], freq='M').map(lambda d: d.replace(day=1))

# create the dash app
# port 8050 by default
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# I need to learn better pandas naming schemes
# should be a lambda
def monthly_return(prices):
    """
    Returns the difference between the first and last value of the data frame

    Parameters
    __________
    prices: pandas.DataFrame

    Returns
    _______
    float
    """
    return prices.iloc[-1] - prices.iloc[0]

app.layout = html.Div(children=[
    html.H4(children='Commodity Data'),
    # generate_table(df)
    dcc.Dropdown(
        id='commodity-selector',
        options=[{'label': h, 'value': h} for h in headers]
    ),
    dcc.Graph(
        id='commodity-graph'
    )
])

@app.callback(
    Output('commodity-graph', 'figure'),
    [Input('commodity-selector', 'value')])
def update_dash(index):
      # set a default index if none is selected
      # used for app startup
      index = index if index else headers[1]
      print('Selecting index: {index}'.format(index=index))

      # split index data from base df
      df_index = df[['DATE', 'YEAR', 'MONTH', index if index else headers[1]]]

      monthly_return_data = df_index.groupby(['YEAR', 'MONTH']).apply(monthly_return)

      # split datas into scatter (price) and monthly bar (monthly return, volatility, etc...)
      scatter_data = [df[index]]
      monthly_bar_data = []

      # print(monthly_return_data[index])

      # create the plotly layout
      return {
            'data':[
                {'x': date_series, 'y': df[index], 'type': 'line', 'name': 'Price'},
                {'x': start_of_month_series, 'y': monthly_return_data[index], 'type': 'bar', 'name': 'Monthly return'},
                # {'x': start_of_month_series, 'y': [92, 63, 21, 14, 51], 'type': 'bar', 'name': 'Boats'},
            ],
            'layout': {
                'title': 'hoopla'
            }
        }

# run app server on main
if __name__ == '__main__':
    app.run_server(debug=True)

