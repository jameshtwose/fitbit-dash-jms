from dash import Dash, dcc, html
from utils import get_data
import dash_bootstrap_components as dbc

sleep_df = get_data(data_type="sleep_daily")
sleep_list = sleep_df.select_dtypes("number").columns.tolist()

activity_df = get_data(data_type="activity_daily")
activity_list = activity_df.select_dtypes("number").columns.tolist()

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    # "display": "none"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "30rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("itsamejms' health data", className="display-4"),
        html.Hr(),
        html.H6("Activity Options"),
        dcc.Dropdown(
            options=activity_list,
            value=[],
            multi=True,
            id="activity-string-dropdown",
        ),
        html.H6("Sleep Options"),
        dcc.Dropdown(
            options=sleep_list,
            value=[],
            multi=True,
            id="sleep-string-dropdown",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home/ Descriptives", href="/", active="exact"),
                dbc.NavLink("Activity Info", href="/page-1", active="exact"),
                dbc.NavLink("Sleep Info", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.Div(
            [html.Img(src=r"assets/logo.png", alt="logo", width=80)], style={"textAlign": "center"}
        ),
        html.Div(
            [
                html.A(
                    children="Created by James Twose",
                    href="https://services.jms.rocks",
                    style={"color": "#5f4a89"},
                )
            ],
            style={"textAlign": "center", "color": "#5f4a89", "marginTop": 40, "marginBottom": 40},
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div([html.Div(id="output-data-upload")], id="page-content", style=CONTENT_STYLE)
