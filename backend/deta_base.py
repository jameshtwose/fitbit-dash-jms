# %%
from deta import Deta
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from ast import literal_eval
import os
from glob import glob

from utils import (
    dict_to_df,
    insert_values,
    delete_values,
    activity_daily_column_list,
    sleep_daily_column_list,
)

# %%
_ = load_dotenv(find_dotenv())
deta = Deta(os.environ["health_deta_project_key"])

# %%
# FITBIT ACTIVITY TOTAL
activity_total_db = deta.Base("fitbit_activity_total")
activity_total_df = pd.read_csv(glob("data/*_lifetime*")[0], index_col=0)[["total"]].T.reset_index(
    drop=True
)

# %%
# FITBIT ACTIVITY BEST
activity_best_db = deta.Base("fitbit_activity_best")
_df = pd.read_csv(glob("data/*_best*")[0], index_col=0)[["total"]].T.reset_index(drop=True)
activity_best_df = pd.concat([dict_to_df(_df[x]) for x in _df.columns.tolist()], axis=1)

# %%
# FITBIT ACTIVITY DAILY
activity_daily_db = deta.Base("fitbit_activity_daily")
activity_daily_df = pd.read_csv(glob("data/activity_2*")[0], index_col=0).loc[
    :, activity_daily_column_list
]

# %%
# FITBIT SLEEP DAILY
sleep_daily_db = deta.Base("fitbit_sleep_daily")
sleep_daily_df = (
    pd.read_csv(glob("data/sleep*")[0], index_col=0)
    .loc[:, sleep_daily_column_list]
    .drop_duplicates()
    .reset_index(drop=True)
)

# %%
# FITBIT SLEEP LEVELS
sleep_levels_db = deta.Base("fitbit_sleep_levels")
_df = pd.read_csv(glob("data/sleep*")[0], index_col=0).reset_index(drop=True)
sleep_levels_df = pd.concat(
    [
        pd.DataFrame(literal_eval(_df.loc[x, "levels"]))
        for x in range(_df.shape[0])
        if pd.DataFrame(literal_eval(_df.loc[x, "levels"])).shape[1] == 3
    ]
)

# %%
db_df_dict = {
    activity_total_db: activity_total_df,
    activity_best_db: activity_best_df,
    activity_daily_db: activity_daily_df,
    sleep_daily_db: sleep_daily_df,
    sleep_levels_db: sleep_levels_df,
}

# %%
for db in db_df_dict:
    delete_values(db=db)
    insert_values(db=db, data=db_df_dict[db])

# %%
# # Fetch data and reassign data types/ drop default key column
# df = (
#     pd.DataFrame(activity_total_db.fetch().items)
#     #  .assign(**{"date": lambda d: pd.to_datetime(d["date"]).dt.date})
#     .drop("key", axis=1)
#     #  .sort_values(by="date")
#     .reset_index(drop=True)
# )
