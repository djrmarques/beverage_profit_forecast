# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from plot_functions import plot_cities_forecast, plot_profit_per_city, plot_profit_per_container, plot_profit_per_capita

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Beverage Sales Dashboard'

# Read the data
df = pd.read_csv("data/profit_forecast/raw_data.csv", index_col=0)
df.index = pd.to_datetime(df.index)

# Read the forecasting data
forecasts = pd.read_csv("data/profit_forecast/forecasts.csv", index_col=0)
forecasts.index = pd.to_datetime(forecasts.index)

server = app.server

# Create the webapp
app.layout = html.Div(children=[
    html.H1(children='Beverage Sales Dashboard'),

    dcc.Graph(id='Forecasting plot', figure=plot_cities_forecast(forecasts)),

    html.P(),

    dcc.Graph(id='profit-per-container'),
    dcc.Slider(
        id='container-slider',
        min=df.index.year.min(),
        max=df.index.year.max(),
        value=df.index.year.max(),
        marks={str(year): str(year) for year in df.index.year},
        step=None
    ),

    dcc.Graph(id='profit-per-city'),
    dcc.Slider(
        id='city-slider',
        min=df.index.year.min(),
        max=df.index.year.max(),
        value=df.index.year.max(),
        marks={str(year): str(year) for year in df.index.year},
        step=None
    ),

    dcc.RadioItems(
    id="profit_radio",
    options=[
        {'label': 'Total Profit', 'value': 'tp'},
        {'label': 'Profit per Capita', 'value': 'ppc'},
    ],
    labelStyle={'display': 'inline-block'},
    value='ppc',
    ),


])


@app.callback(
    Output('profit-per-container', 'figure'),
    [Input('container-slider', 'value')])
def update_cities(selected_year):
    return plot_profit_per_container(selected_year, df)

@app.callback(
    Output('profit-per-city', 'figure'),
    [Input('city-slider', 'value'), Input('profit_radio', 'value')])
def update_containers(selected_year: int, graph_type: str):
    if graph_type == "tp":
        return plot_profit_per_city(selected_year, df)
    else:
        return plot_profit_per_capita(selected_year, df)



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)