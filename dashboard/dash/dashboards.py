from dash import Dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


def add_dash(server):

    external_stylesheets = ['']
    external_scripts = ['']

    dashboards = Dash(server=server,
                      external_stylesheets=external_stylesheets,
                      external_scripts=external_scripts,
                      routes_pathname_prefix='/dashboards/')

    dashboards.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
        Dash: A web application framework for Python.
    '''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2],
                        'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5],
                     'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])

    return dashboards.server
