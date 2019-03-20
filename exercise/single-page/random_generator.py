# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from app import app

import numpy as np
import pandas as pd
import json
import dash_table as dt

import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

tabs_styles = {
    'height': '24px'
}

tab_style = {
    'borderTop': 'none',
    'borderRight': 'none',
    'borderLeft': 'none',
    'padding': '6px',
    'color': '#337ab7',
    'backgroundColor': 'white',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderRight': '1px solid #d6d6d6',
    'borderLeft': '1px solid #d6d6d6',
    'color': '#555',
    'padding': '6px'
}

title = 'Random generator'

default_data = json.dumps(np.random.normal(size=50).tolist())


def generate_table(dict, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(key) for key in dict.keys()])] +

        # Body
        [html.Tr( [html.Td(dict[key]) for key in dict.keys()] )]
    )


layout_plot = html.Div([
                    dcc.Graph(id='rg-graph'),
                ])
layout_summary = html.Div([
                    html.Div(id='rg-summary'),
                ])
layout_table = html.Div([
                    dt.DataTable(id='rg-table',columns=[{'id': 0, 'name': 'data'}]),
                ])

layout = html.Div([
            html.Div(default_data, id="rg-data", style={'display': 'none'}),
            html.Div([
                dcc.Tabs(id="rg-tabs", value='rg-plot', children=[
                    dcc.Tab(label='Plot', value='rg-plot',style=tab_style, selected_style=tab_selected_style,
                            children=layout_plot),
                    dcc.Tab(label='Summary', value='rg-summary',style=tab_style, selected_style=tab_selected_style,
                            children=layout_summary),
                    dcc.Tab(label='Table', value='rg-table',style=tab_style, selected_style=tab_selected_style,
                            children=layout_table),
                ]),
                html.Div(id='rg-tabs-content'),
                ],
                style={'width': '65%',  'float': 'left'}
            ),
            html.Div([
                html.Div([
                html.Label('Number of samples'),
                dcc.Slider(id='rg-nsample',
                    min=10,
                    max=100,
                    marks={i: str(i) for i in range(10, 110, 10)},
                    value=50)
                ], style={'marginBottom':'30px'}),
                html.Button('Go!', id='rg-go'),
                html.Div([
                html.Label('Number of bins'),
                dcc.Slider(id='rg-nbins',
                    min=1,
                    max=50,
                    marks={i: str(i) for i in range(1, 50, 5)},
                    value=30,
                )], style={'marginTop':'30px','marginBottom':'30px'}),
                ],
                style={'width': '30%', 'float': 'right', 'padding': '20px'}
            ),
            html.Div(style={'clear': 'both'}),
            ],
            style={'marginTop': '25px'}
        )


@app.callback(Output('rg-data', 'children'),[Input('rg-go', 'n_clicks')],[State('rg-nsample', 'value')])
def generate_data(n_clicks, n):
    data = np.random.normal(size=n)
    return json.dumps(data.tolist())


@app.callback(
    Output('rg-graph', 'figure'),
    [Input('rg-data', 'children'), Input('rg-nbins', 'value'), Input('rg-tabs', 'value')]
)
def update_rg_graph(json_data, nbins, tab):
    if tab != 'rg-plot' or json_data is None:
        return {}
    data = np.array(json.loads(json_data))
    return  {
            'data': [
                go.Histogram(
                    x=data,
                    nbinsx=nbins,
                    marker=dict(
                        color='white',
                        line=dict(
                            color='black',
                            width=1
                        )
                    ),
                    opacity=0.75
                ),
            ],
            'layout': go.Layout(
                    title='Random Generation',
                    xaxis=dict(
                        title='samples()'
                    ),
                    yaxis=dict(
                        title='Frequency'
                    ),
                    bargap=0.2,
                    bargroupgap=0.1
                )
        }


@app.callback(
    Output('rg-summary', 'children'),
    [Input('rg-data', 'children'), Input('rg-tabs', 'value')]
)
def update_rg_summary(json_data, tab):
    if tab != 'rg-summary' or json_data is None:
        return {}
    data = np.array(json.loads(json_data))
    ps = pd.Series(data)
    psd = ps.describe()
    return generate_table(psd.round(decimals=5).to_dict())


@app.callback(
    Output('rg-table', 'data'),
    [Input('rg-data', 'children'), Input('rg-tabs', 'value')]
)
def update_rg_table(json_data, tab):
    if tab != 'rg-table' or json_data is None:
        return {}
    data = np.array(json.loads(json_data))
    df = pd.DataFrame(data=data)
    return df.to_dict('rows')
