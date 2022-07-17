import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from assets.time_delta_values import TimeDeltaValues


td = TimeDeltaValues()

navbar_img = "https://i.ibb.co/17PHQ7D/large-D.png"

contributors = [
    ("Joel Bäcker", "Skattmästare 21, Skattförman 22"),
    ("Jacob Säll Nilsson", "Vice Skattmästare 21"),
    ("Axel Svensson", "Skattförman 21, Vice Skattmästare 22"),
]


def create_options(options):
    return [{"label": o.capitalize(), "value": o.lower()} for o in options]


def creat_credits_list(people):
    s = ""
    for name, roles in people:
        s += f"- {name} ({roles})\n"
    return s


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
                    options=td.options(),
                    value="daily",
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
                        # dcc.DatePickerRange(), could use
                        dcc.Input(
                            placeholder=td.patterns()["daily"]["placeholder"],
                            pattern=td.patterns()["daily"]["pattern"],
                            id="start-date-inp",
                            style={"marginRight": "10px"},
                        ),
                        dcc.Input(
                            placeholder=td.patterns()["daily"]["placeholder"],
                            pattern=td.patterns()["daily"]["pattern"],
                            id="end-date-inp",
                            style={"marginRight": "10px"},
                        ),
                    ],
                ),
            ]
        ),
        html.P(),
        html.H5("Result"),
        html.P(),
        html.H5("Credits"),
        html.P("Made by:"),
        dcc.Markdown(creat_credits_list(contributors)),
    ],
    style={"marginLeft": "20px", "marginRight": "20px", "marginTop": "10px"},
)


layout = html.Div(
    [
        navbar,
        generate_intakt,
    ]
)
