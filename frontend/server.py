import dash_bootstrap_components as dbc
from dash import Dash

external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, 
           title="Fitbit Dashboard", 
           external_stylesheets=external_stylesheets, 
           suppress_callback_exceptions=True
           )

server = app.server

