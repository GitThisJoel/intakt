import sys, os
import pathlib

f_path = str(pathlib.Path(__file__).parent.resolve())
sys.path.append(f_path + "/../main")

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import flask

from intakt_page import layout

# from app import app, server
app = dash.Dash(
    name="intakt",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    server=flask.Flask(__name__),
)
# app.config.suppress_callback_exceptions = True
server = app.server

app.title = "D-sek intakt"
# app._favicon = "../webpage/assets/favicon.ico"

template = "plotly_white"

app.layout = html.Div(
    [
        layout,
    ]
)

if __name__ == "__main__":
    app.run_server(
        debug=True,
        dev_tools_hot_reload=True,
        host="0.0.0.0",
        port=1999,
    )
