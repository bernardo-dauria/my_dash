# -*- coding: utf-8 -*-
from app import app
import dash_core_components as dcc
import dash_html_components as html

import msleep, random_generator, references
from dash.dependencies import Input, Output


navs_styles = {
    'height': '24px'
}

nav_style = {
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#f8f8f8',
    'padding': '6px',
    'color': '#777'
}

nav_disabled_style = nav_style.copy()
nav_disabled_style.update({'width': '100px'})

nav_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#e7e7e7',
    'color': '#555',
    'padding': '6px'
}

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-2', children=[
        dcc.Tab(label='Dash app', value='tab-0', disabled='True', style=nav_style, disabled_style=nav_disabled_style),
        dcc.Tab(label=msleep.title, value='tab-1',style=nav_style, selected_style=nav_selected_style),
        dcc.Tab(label=random_generator.title, value='tab-2', style=nav_style, selected_style=nav_selected_style),
        dcc.Tab(label=references.title, value='tab-3', style=nav_style, selected_style=nav_selected_style),
    ]),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return msleep.layout
    elif tab == 'tab-2':
        return random_generator.layout
    elif tab == 'tab-3':
        return references.layout


if __name__ == '__main__':
    app.run_server(debug=True)