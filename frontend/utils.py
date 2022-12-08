import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, dash_table
from deta import Deta
from dotenv import load_dotenv, find_dotenv
import os
from jmspack.frequentist_statistics import correlation_analysis

plot_color_list = [
    "rgba(91, 22, 106, 1)",
    "rgba(124, 213, 77, 1)",
    "rgba(59, 12, 71, 1)",
    "rgba(138, 12, 184, 1)",
    "rgba(18, 139, 177, 1)",
    "rgba(35, 206, 217, 1)",
    "rgba(35, 128, 15, 1)",
    "rgba(143, 56, 22, 1)",
    "rgba(219, 78, 109, 1)",
    "rgba(84, 12, 34, 1)",
]


_ = load_dotenv(find_dotenv())
deta = Deta(os.environ["health_deta_project_key"])


def get_data(data_type="sleep_daily"):
    if data_type == "sleep_daily":
        sleep_daily_db = deta.Base("fitbit_sleep_daily")

        # Fetch data and reassign data types/ drop default key column
        df = (
            pd.DataFrame(sleep_daily_db.fetch().items)
            .drop("key", axis=1)
            .rename(columns={"dateOfSleep": "date"})
            .sort_values(by="date")
            .assign(**{"date": lambda d: pd.to_datetime(d["date"])})
            .reset_index(drop=True)
        )
    elif data_type == "activity_daily":
        activity_daily_db = deta.Base("fitbit_activity_daily")

        df = (
            pd.DataFrame(activity_daily_db.fetch().items)
            .drop("key", axis=1)
            .sort_values(by="date")
            .assign(**{"date": lambda d: pd.to_datetime(d["date"])})
            .reset_index(drop=True)
        )
    elif data_type == "activity_best":
        activity_best_db = deta.Base("fitbit_activity_best")

        df = (
            pd.DataFrame(activity_best_db.fetch().items).drop("key", axis=1).reset_index(drop=True)
        )
    elif data_type == "activity_total":
        activity_best_db = deta.Base("fitbit_activity_total")

        df = (
            pd.DataFrame(activity_best_db.fetch().items).drop("key", axis=1).reset_index(drop=True)
        )
    return df


def create_table(data):
    return dash_table.DataTable(
        data=data.to_dict("records"),
        columns=[{"name": i, "id": i} for i in data.columns],
        style_header={"backgroundColor": "#5f4a89"},
        sort_action="native",
        filter_action="native",
        row_deletable=True,
        export_format="csv",
        export_headers="display",
        merge_duplicate_headers=True,
        page_size=10,
    )


def create_line_plot(data, data_type, features):
    fig = px.line(
        data_frame=data,
        x="date",
        y=features,
        markers=True,
        color_discrete_sequence=plot_color_list,
    )
    fig.update_layout(
        title=f"Fitbit data, data type == {data_type}, feature choice == {features}",
        xaxis_title="Date",
        yaxis_title=data_type,
    )

    return fig


def create_heatmap(data, title, x_title, y_title):
    fig = px.imshow(img=data, text_auto=".2f", aspect="auto")
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=False,
        width=1000,
        height=700,
        autosize=False
    )
    return fig


def parse_descriptives(data, title):
    return html.Div([html.H5(title), create_table(data), html.Hr()])


def parse_correlation():
    activity_df = get_data(data_type="activity_daily")
    sleep_df = get_data(data_type="sleep_daily")
    activity_list = activity_df.set_index("date").select_dtypes("number").columns.tolist()
    sleep_list = sleep_df.set_index("date").select_dtypes("number").columns.tolist()

    # %%
    df = pd.merge(
        activity_df.set_index("date")[activity_list],
        sleep_df.set_index("date")[sleep_list],
        left_index=True,
        right_index=True,
        how="inner",
    )

    cor_dict = correlation_analysis(data=df, col_list=activity_list, row_list=sleep_list)
    cor_summary = parse_descriptives(
        data=cor_dict["summary"].round(3), title="Correlation between activity and sleep values"
    )
    cor_heat = create_heatmap(
        data=cor_dict["r-value"],
        title="Correlation between activity and sleep values",
        x_title="Activity Values",
        y_title="Sleep Values",
    )

    return html.Div([cor_summary, dcc.Graph(figure=cor_heat)])


def parse_time_plots(data, data_type, features):
    if features == []:
        feature_list = data.select_dtypes("number").columns.tolist()
        line_fig = create_line_plot(data, data_type, features=feature_list)
    else:
        line_fig = create_line_plot(data, data_type, features)
    return html.Div(
        [
            html.H6(f"Lineplot of {data_type} data"),
            dcc.Graph(figure=line_fig),
        ]
    )
