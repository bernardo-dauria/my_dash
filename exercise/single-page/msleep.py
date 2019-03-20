# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table as dt

from app import app
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go

df_url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv'
df = pd.read_csv(df_url)
df_vore = df['vore'].dropna().sort_values().unique()
opt_vore = [{'label': x + 'vore', 'value': x} for x in df_vore]

title = 'msleep'

layout = html.Div([
            html.Div([
                html.Label('Plot by type of alimentation'),
                dcc.Dropdown(
                    id='my-dropdown',
                    options=opt_vore,
                    value=df_vore[0]
                )
            ],
                style={'width': '20%',  'float': 'left', 'backgroundColor': '#f8f8f8', 'padding': '10px'}
            ),
            html.Div([
                dcc.Graph(id='my-graph'),
                dt.DataTable(id='my-table', columns=[{"name": i, "id": i} for i in df.columns])
            ],
                style={'width': '65%', 'float': 'right', 'marginRight':'10%'}
            ),

            html.Div(style={'clear': 'both'})
            ],
            style={'marginTop': '25px'}
        )


@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    [Input(component_id='my-dropdown', component_property='value')]
)
def update_output_graph(input_value):
    return  {
                'data': [
                    go.Scatter(
                        x=df[df['vore'] == i]['bodywt'] if i == input_value else [],
                        y=df[df['vore'] == i]['sleep_total'] if i == input_value else [],
                        text=df[df['vore'] == i]['name'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df_vore
                ],
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'Body weight (kg)'},
                    yaxis={'title': 'Total daily sleep time (hr)'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest',
                    dragmode='lasso'
                )
            }


@app.callback(
    Output('my-table', 'data'),
    [Input('my-graph', 'selectedData')])
def display_selected_data(selected_data):
    if selected_data is None or len(selected_data) == 0:
        return {}

    points = selected_data['points']
    if len(points) == 0:
        return {}

    names = [x['text'] for x in points]
    return df[df['name'].isin(names)].to_dict("rows")