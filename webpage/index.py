import sys, os
import pathlib

f_path = str(pathlib.Path(__file__).parent.resolve())
sys.path.append(f_path + "/../main")

from dash import html
from dash.dependencies import Input, Output, State

from intakt_page import layout
import callbacks  # load all callbacks
from app import app

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
