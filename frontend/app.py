from server import app, server
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from sidebar import sidebar, content, activity_df, sleep_df

from utils import parse_time_plots, parse_descriptives, get_data, parse_correlation
import pandas as pd

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


def update_descriptives():
    activity_best_df = get_data(data_type="activity_best")
    best_info = parse_descriptives(
        data=activity_best_df, title="The highest activity data and the dates they occurred"
    )
    activity_total_df = get_data(data_type="activity_total")
    total_info = parse_descriptives(
        data=activity_total_df, title="The total activity data"
    )

    correlation_info = parse_correlation()
    children = html.Div([best_info, total_info, correlation_info])
    return children


@app.callback(
    Output("output-data-activity", "children"),
    Input("activity-string-dropdown", "value"),
)
def update_time_plots_activity(features_list):
    children = parse_time_plots(
        data=activity_df, data_type="Activity Daily", features=features_list
    )
    return children


@app.callback(
    Output("output-data-sleep", "children"),
    Input("sleep-string-dropdown", "value"),
)
def update_time_plots_sleep(features_list):
    children = parse_time_plots(data=sleep_df, data_type="Sleep Daily", features=features_list)
    return children


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        # return html.P("This is the content of the home page!")
        output = html.Div(update_descriptives())
        return output
    elif pathname == "/page-1":
        return html.Div(id="output-data-activity")
    elif pathname == "/page-2":
        return html.Div(id="output-data-sleep")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True, threaded=True)
