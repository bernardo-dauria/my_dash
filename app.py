# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/) 
specification of Markdown.  
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''


df_url = 'https://forge.scilab.org/index.php/p/rdataset/source/file/master/csv/ggplot2/msleep.csv'
df = pd.read_csv(df_url)
df_vore = df['vore'].dropna().sort_values().unique()
opt_vore = [{'label': x + 'vore', 'value': x} for x in df_vore]

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div(children=[
    dcc.Markdown(children=markdown_text),

    dcc.Graph(id='my-graph'),
    dcc.Graph(id='my-box-plot'),

    html.Div([
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(
            id='my-multi-dropdown',
            options= opt_vore,
            value= df_vore[0:2],
            multi= True
        ),

        html.Div([
            html.Div(
                dcc.RangeSlider(
                    id='my-slider',
                    min= 0, max= 100, value=[0,100],
                    step= 0.1,
                ),
                style={
                    'width': '60%',
                    'display': 'inline-block',
                    'paddingLeft': '10%',
                    'paddingRight': '10%'
                }
            ),
            html.Button('Update filter', id='my-button')
        ],
            style={
                'marginTop': '5%',
                'marginBottom': '5%'
            }
        )
    ])
])

@app.callback(
    [Output('my-graph', 'figure'),
     Output('my-box-plot', 'figure'),],
    [Input('my-multi-dropdown', 'value'),
     Input('my-button', 'n_clicks')],
    [State('my-slider', 'value')]
)
def update_output_graph(input_value, n_clicks, slider_range):
    if (len(slider_range) == 2):
        l, h = slider_range
    else :
        l, h = 0, 100;
    data_filtered = df[df['sleep_total'].between(l,h)]
    return  {
                'data': [
                    go.Scatter(
                        x=data_filtered[data_filtered['vore'] == i]['bodywt'] if i in input_value else [],
                        y=data_filtered[data_filtered['vore'] == i]['sleep_total'] if i in input_value else [],
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
                    hovermode='closest'
                )
            },            \
            {
                'data': [ go.Box(
                            y= df[df['vore'] == i]['sleep_total'],
                            name= i + 'vore'
                        ) if i in input_value else []
                          for i in df_vore ]
            }

@app.callback(
    [Output('my-slider', 'min'), Output('my-slider', 'max'), Output('my-slider', 'value'), Output('my-slider', 'marks')],
    [Input('my-multi-dropdown', 'value')]
)
def update_slider(input_value):
    def round(x):
        return int(x) if x % 0.1 < 0.1 else x
    data = df[df.vore.isin(input_value)]['sleep_total']
    min = round(data.min())
    max = round(data.max())
    mean = round(data.mean())
    low = round((min + mean)/2)
    high = round((max + mean) / 2)
    marks = {min: {'label': min, 'style': {'color': '#77b0b1'}},
             max: {'label': max, 'style': {'color': '#77b0b1'}}}
    return min, max,  [low, high], marks


if __name__ == '__main__':
    app.run_server(debug=True)