from jmspack.utils import apply_scaling, JmsColors
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

from utils import get_data

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

db_list = ["activity_daily", "sleep_daily"][:-1]

df = get_data(data_type=db_list[0])

features_list = df.select_dtypes("number").columns.tolist()

app.layout = html.Div(
    [
        html.H1(
            id="H1",
            children="FitBit Numbers",
            style={"textAlign": "center", "marginTop": 40, "marginBottom": 40},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="db_choice",
                    options=[
                        {"label": i.title().replace("_", " "), "value": i} for i in db_list
                    ],
                    value=db_list[0],
                )
            ],
            style={"width": "20%", "display": "inline-block", "padding": "5px"},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="feature_choice",
                    options=[
                        {"label": i.title().replace("_", " "), "value": i} for i in features_list
                    ],
                    value=features_list[0],
                    multi=True,
                )
            ],
            style={"width": "20%", "display": "inline-block", "padding": "5px"},
        ),
        dcc.Graph(id="line_plot"),
        html.Div(
            html.A(
                children="Created by James Twose",
                href="https://services.jms.rocks",
                style={"color": "#743de0"},
            ),
            style={"textAlign": "center", "color": "#743de0", "marginTop": 40, "marginBottom": 40},
        ),
    ]
)


@app.callback(
    Output(component_id="line_plot", component_property="figure"),
    [
        Input(component_id="db_choice", component_property="value"),
        Input(component_id="feature_choice", component_property="value"),
    ],
)
def graph_update(db_choice, feature_choice):
    plot_color_list = JmsColors.to_list()
    if feature_choice == []:
        fig = px.line(
            data_frame=df,
            x="date",
            y=features_list[:-1],
            markers=True,
            color_discrete_sequence=plot_color_list,
        )
        fig.update_layout(
            title=f"Fitbit data, db == {db_choice}, feature choice == {features_list}",
            xaxis_title="Date",
            yaxis_title="Sleep Value",
        )
    else:
        fig = px.line(
            data_frame=df,
            x="date",
            y=feature_choice,
            markers=True,
            color_discrete_sequence=plot_color_list,
        )

        fig.update_layout(
            title=f"Fitbit data, db == {db_choice}, feature choice == {feature_choice}",
            xaxis_title="Date",
            yaxis_title="Sleep Value",
        )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, threaded=True)
