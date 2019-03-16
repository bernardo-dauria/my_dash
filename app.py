# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

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

    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['vore'] == i]['bodywt'],
                    y=df[df['vore'] == i]['sleep_total'],
                    text=df[df['vore'] == i]['name'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.vore.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'Body weight (kg)'},
                yaxis={'title': 'Total daily sleep time (hr)'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)