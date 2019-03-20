# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

title = 'References'

markdown_text = '''
# 

- [Dash Tutorial](https://dash.plot.ly/installation)
- [Dash User Guide](https://dash.plot.ly/)
- [GitHub repository](https://github.com/bernardo-dauria/my_dash)
'''

layout = html.Div(
        dcc.Markdown(children=markdown_text)
    )