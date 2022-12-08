# %%
from deta import Deta
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os
from glob import glob
from ast import literal_eval

# %%
_ = load_dotenv(find_dotenv())
deta = Deta(os.environ["health_deta_project_key"])


# %%
def dict_to_df(col):
    df = pd.DataFrame(literal_eval(col[0]), index=[0])
    df.columns = [f"{col.name}_{x}" for x in df.columns.tolist()]
    return df

# %%
# FITBIT ACTIVITY TOTAL
activity_total_db = deta.Base("fitbit_activity_total")
df = (pd.read_csv(glob("data/*_lifetime*")[0], index_col=0)
[["total"]].T.reset_index(drop=True))
# inserted_values = [activity_total_db.insert(data=row_to_insert) for row_to_insert in df.to_dict(orient="records")]

# %%
# FITBIT ACTIVITY BEST
activity_best_db = deta.Base("fitbit_activity_best")
_df = (pd.read_csv(glob("data/*_best*")[0], index_col=0)
[["total"]].T.reset_index(drop=True))
df = pd.concat([dict_to_df(_df[x]) for x in _df.columns.tolist()], axis=1)
# inserted_values = [activity_best_db.insert(data=row_to_insert) for row_to_insert in df.to_dict(orient="records")]

# %%
# FITBIT ACTIVITY DAILY
column_list = ['date', 'caloriesOut', 'distances', 'steps', 'activityCalories',
       'marginalCalories', 'sedentaryMinutes', 'lightlyActiveMinutes',
       'fairlyActiveMinutes', 'veryActiveMinutes']
activity_daily_db = deta.Base("fitbit_activity_daily")
df = (pd.read_csv(glob("data/activity_2*")[0], index_col=0)
.loc[:, column_list])
# inserted_values = [activity_daily_db.insert(data=row_to_insert) for row_to_insert in df.to_dict(orient="records")]

# %%
# FITBIT SLEEP DAILY
column_list = ['minutesAfterWakeup', 'efficiency', 'minutesAwake', 'duration',
       'minutesAsleep', 'timeInBed', 'dateOfSleep', 'endTime',
       'startTime']
sleep_daily_db = deta.Base("fitbit_sleep_daily")

df = (pd.read_csv(glob("data/sleep*")[0], index_col=0)
.loc[:, column_list]
.drop_duplicates()
.reset_index(drop=True)
)
# inserted_values = [sleep_daily_db.insert(data=row_to_insert) for row_to_insert in df.to_dict(orient="records")]

# %%
# FITBIT SLEEP LEVELS
sleep_levels_db = deta.Base("fitbit_sleep_levels")

_df = (pd.read_csv(glob("data/sleep*")[0], index_col=0)
.reset_index(drop=True)
)

df = (pd.concat([pd.DataFrame(literal_eval(_df.loc[x, "levels"]))
for x in range(_df.shape[0])
if pd.DataFrame(literal_eval(_df.loc[x, "levels"])).shape[1]==3])
# .groupby(["dateTime", "level"])
# .sum()
)

# inserted_values = [sleep_levels_db.insert(data=row_to_insert) for row_to_insert in df.to_dict(orient="records")]

# %%
# Fetch data and reassign data types/ drop default key column
df = (pd.DataFrame(activity_total_db.fetch().items)
#  .assign(**{"date": lambda d: pd.to_datetime(d["date"]).dt.date})
 .drop("key", axis=1)
#  .sort_values(by="date")
 .reset_index(drop=True)
 )
# %%
df
# %%
