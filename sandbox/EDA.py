# %%
import pandas as pd
import seaborn as sns
import plotly.express as px
from pyunicorn.timeseries import RecurrencePlot
from jmspack.utils import silence_stdout

# %%
df = sns.load_dataset("iris")

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
rm_df = pd.DataFrame(new_matrix, index=df.index[4:], columns=df.index[4:])
# %%
_ = sns.heatmap(rm_df)
# %%
fig = px.imshow(rm_df, color_continuous_scale=["white", "rgba(91, 22, 106, 1)"])
fig.update_yaxes(showticklabels=False)
fig.show()
