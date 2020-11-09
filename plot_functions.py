import numpy as np
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict
import seaborn as sns

def plot_cities_forecast(forecasts: Dict[str, pd.DataFrame]):
    """ Creates the plotly figure for the cities forecast """
    
    # Get color scheme from seaborn
    city_color_dictionary = dict(zip(forecasts["city"].unique(), [f"rgb{c}" for c in sns.color_palette("deep")]))

    fig = go.Figure()
    for city in forecasts["city"].unique():

        # Plot real values
        fig.add_trace(go.Scatter(x=forecasts[forecasts["city"]==city].index, 
                                 y=forecasts.loc[forecasts["city"]==city, "real_values"], 
                                 name=city, 
                                 legendgroup=city,
                                 line=dict(color=city_color_dictionary[city]),
                                 mode='lines'))
        # Plot Predictions
        forecasting_df = forecasts.loc[(forecasts["city"]==city) & (forecasts["real_values"].isna()), :]
        fig.add_trace(go.Scatter(x=forecasting_df.index, 
                             y=forecasting_df["forecast"], 
                             name=city, 
                             legendgroup=city,
                             mode='lines+markers',
                             line=dict(color=city_color_dictionary[city], width=1, dash='dot'),
                             error_y=dict(type='data', array=forecasting_df["error"], visible=True),    
                             showlegend=False))
        
    # Add a vertical line to mark the forecasting period
    fig.add_shape(type='line',
                yref="paper",
                xref="x",
                x0=forecasts.loc[forecasts["city"]==city, "real_values"].dropna().index.max(),
                y0=0,
                x1=forecasts.loc[forecasts["city"]==city, "real_values"].dropna().index.max(),
                y1=1,
                line=dict(color='black', width=0.5, dash="dash"))
    
    # Add annoation on the forecast line 
    fig.add_annotation(
                x=forecasts.loc[forecasts["city"]==city, "real_values"].dropna().index.max(),
                y=1,
                yref='paper',
                xanchor="right",
                yanchor="top",
                showarrow=False,
                textangle=-90,
                text="Forecast Start")

    fig.layout.title.text = "Monthly Profit per city."
    fig.layout.yaxis.title = "Profit (€)"
    fig.layout.xaxis.title = "Date"
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(legend_title_text='City')
    return fig

def plot_profit_per_container(year: int, df: pd.DataFrame):
    """ Plots the profit per container per brand on a given year"""
    
    df_ = df.drop(["lat", "long", "capacity"], axis=1).dropna().copy()
    color_dict = dict(zip(["glass-500ml", 'plastic-1.5lt', 'can-330ml'], [f"rgb{c}" for c in sns.color_palette("deep")]))
    
    fig = px.box(df_[df_.index.year == year].dropna().sort_values("container"), x="brand", color="container", color_discrete_map=color_dict, y="profit", title=f"Monthly profit per brand per container on {year}")
    fig.layout.yaxis.title = "Monthly Profit (€)"
    fig.layout.xaxis.title = "Brand"
    return fig

def plot_profit_per_city(year: int, df: pd.DataFrame):
    """ Plots the profit per city on a given year """
    fig = px.bar(df.loc[df.index.year==year,:].groupby("city", as_index=False)["profit"].sum().round().sort_values("profit"), 
                 x="city", 
                 y="profit", 
                 title=f"Total Profit per city on {year}",
                 color_discrete_sequence = [f"rgb{sns.color_palette('deep')[0]}"]
                )
    
    fig.layout.yaxis.title="Profit (€)"
    fig.layout.xaxis.title="City"
    return fig

def plot_profit_per_capita(year: int, df: pd.DataFrame):
    """ Plots the profit per ccapita per city on a given year """
    fig = px.bar(df.loc[df.index.year==year,:].groupby("city", as_index=False)["profit_per_capita"].mean().round(2).sort_values("profit_per_capita"), 
                 x="city", 
                 y="profit_per_capita", 
                 title=f"Profit per capita on {year}",
                 color_discrete_sequence = [f"rgb{sns.color_palette('deep')[0]}"]
                )
    
    fig.layout.yaxis.title="Profit per capita (€)"
    fig.layout.xaxis.title="City"
    return fig

