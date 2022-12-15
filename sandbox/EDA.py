# %%
import pandas as pd
import seaborn as sns
import plotly.express as px
from pyunicorn.timeseries import RecurrencePlot
from jmspack.utils import silence_stdout

# %%
import os
current_wd = os.getcwd()
os.chdir(current_wd.split("sandbox")[0])
from frontend.utils import get_data
os.chdir(current_wd)

# %%
# df = sns.load_dataset("iris")
activity_df = get_data(data_type="activity_daily")
sleep_df = get_data(data_type="sleep_daily")
activity_list = activity_df.set_index("date").select_dtypes("number").columns.tolist()
sleep_list = sleep_df.set_index("date").select_dtypes("number").columns.tolist()
df = pd.merge(
    activity_df.set_index("date")[activity_list],
    sleep_df.set_index("date")[sleep_list],
    left_index=True,
    right_index=True,
    how="inner",
)

# %%
with silence_stdout():
    determinism_column = df.select_dtypes("number").apply(
        lambda x: RecurrencePlot(
            time_series=x.values, metric="manhattan", dim=3, tau=2, recurrence_rate=0.05
        ).determinism(l_min=2)
    )
    laminarity_column = df.select_dtypes("number").apply(
        lambda x: RecurrencePlot(
            time_series=x.values, metric="manhattan", dim=3, tau=2, recurrence_rate=0.05
        ).laminarity(v_min=2)
    )
    diag_entropy_column = df.select_dtypes("number").apply(
        lambda x: RecurrencePlot(
            time_series=x.values, metric="manhattan", dim=3, tau=2, recurrence_rate=0.05
        ).diag_entropy(l_min=2)
    )
# %%
rp_df = (
    pd.concat([determinism_column, laminarity_column, diag_entropy_column], axis=1)
    .reset_index()
    .rename(columns={"index": "feature", 0: "determinism", 1: "laminarity", 2: "diagonal_entropy"})
    .sort_values(by=["determinism", "laminarity"], ascending=False)
)
# %%
best_feature = rp_df["feature"].head(1).values[0]

# %%
best_rm = RecurrencePlot(
    time_series=df[best_feature].values, metric="manhattan", dim=3, tau=2, recurrence_rate=0.05
).recurrence_matrix()
# %%
# rotate the matrix 90 degrees so it starts at day 0 in the bottom left corner
new_matrix = [
    [best_rm[j][i] for j in range(len(best_rm))] for i in range(len(best_rm[0]) - 1, -1, -1)
]
rm_df = pd.DataFrame(new_matrix, index=df.index.sort_values(ascending=False)[:-4], columns=df.index[4:])
# %%
_ = sns.heatmap(rm_df)
# %%
fig = px.imshow(rm_df, 
color_continuous_scale=["white", "rgba(91, 22, 106, 1)"],
origin="lower")
# fig.update_yaxes(showticklabels=False)
fig.show()

# %%

# %%
