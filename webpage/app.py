import dash
import flask
import dash_bootstrap_components as dbc

app = dash.Dash(
    name="intakt",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    server=flask.Flask(__name__),
)
# app.config.suppress_callback_exceptions = True
server = app.server

app.title = "D-sek intakt"
# app._favicon = "../webpage/assets/favicon.ico"
