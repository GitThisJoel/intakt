import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

navbar_img = "https://i.ibb.co/17PHQ7D/large-D.png"


def create_options(options):
    return [{"label": o, "id": o.lower()} for o in options]


navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(src=navbar_img, height="30px"),
                        ),
                        dbc.Col(
                            dbc.NavbarBrand("sektionens intäktsgenerator", className="ms-2"),
                        ),
                    ],
                    justify="left",
                    align="start",
                    className="g-0",
                ),
                # href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            # dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        ],
        fluid=True,
        style={"marginLeft": "10px"},
    ),
    color="dark",
    dark=True,
)

generate_intakt = html.Div(
    [
        html.H5("Select time delta"),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    options=["Daily", "Weekly", "Monthly", "Biannually", "Yearly", "Custom"],
                    value="Daily",
                    id="time-delta-dd",
                ),
                xs=3,
            )
        ),
        html.P(),
        html.H5("Select date range"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Input(
                            placeholder="start date",
                            id="start-date-inp",
                            style={"marginRight": "10px"},
                        ),
                        dcc.Input(
                            placeholder="end date",
                            id="end-date-inp",
                        ),
                    ],
                ),
            ]
        ),
        html.P(),
        html.H5("Result"),
    ],
    style={"marginLeft": "20px", "marginRight": "20px", "marginTop": "10px"},
)


layout = html.Div(
    [
        navbar,
        generate_intakt,
    ]
)
