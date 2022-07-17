import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from index import app
from time_delta_values import TimeDeltaValues

td = TimeDeltaValues()


@app.callback(
    Output("start-date-inp", "placeholder"),
    Output("start-date-inp", "pattern"),
    Output("start-date-inp", "value"),
    Output("end-date-inp", "placeholder"),
    Output("end-date-inp", "pattern"),
    Output("end-date-inp", "value"),
    Input("time-delta-dd", "value"),
)
def change_placeholder(selected_time_delta):
    ph = td.patterns()[selected_time_delta]["placeholder"]
    pat = td.patterns()[selected_time_delta]["pattern"]
    return ph, pat, "", ph, pat, ""
