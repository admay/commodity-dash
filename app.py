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
# use real datetimes
df['DATE'] = pd.to_datetime(df['DATE'])
# add date breakup cols for grouping
df['YEAR'], df['MONTH'], df['DAY'] = df['DATE'].dt.year, df['DATE'].dt.month, df['DATE'].dt.day

# get asset selection dropdown data
headers = list(df)

# and create a date series for the x-axis
date_series = df['DATE']
