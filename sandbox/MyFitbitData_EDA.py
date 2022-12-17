# %%
from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
from datetime import datetime

from deta import Deta
from dotenv import load_dotenv, find_dotenv
import os
current_wd = os.getcwd()
os.chdir(current_wd.split("sandbox")[0])
from frontend.utils import get_data
os.chdir(current_wd)

# %%
_ = load_dotenv(find_dotenv())
deta = Deta(os.environ["health_deta_project_key"])

# %%
# FITBIT ACTIVITY DAILY
activity_df = get_data(data_type="activity_daily")
sleep_df = get_data(data_type="sleep_daily")

# %%
# OXYGEN
ox_df = (pd.concat([(pd.read_csv(file)
            .agg({"timestamp": lambda x: x.iloc[0],
                  "Infrared to Red Signal Ratio": "var"})) for file in glob("data/MyFitbitData/Oxygen/*")],
          axis=1)
      .T
      .assign(**{"date": lambda d: pd.to_datetime(d["timestamp"]).dt.date})
      .drop("timestamp", axis=1)
      .sort_values(by="date")
      .set_index("date")
      .reset_index()
      )
# %%
_ = plt.figure(figsize=(15, 5))
_ = sns.lineplot(data=ox_df, x="date", y="Infrared to Red Signal Ratio")
# %%
# PHYSICAL ACTIVITY
heart_zone_mins_df = pd.concat([(pd.read_csv(file)
.assign(**{"date": lambda d: pd.to_datetime(d["date_time"]).dt.date})
.drop("date_time", axis=1)
.groupby(["date", "heart_zone_id"])
.sum()
.reset_index()
.pivot_table(values="total_minutes", index="date", columns="heart_zone_id")
) for file in glob("data/MyFitbitData/Physical Activity/Active Zone*.csv")]).sort_values(by="date").reset_index()

# %%
_ = plt.figure(figsize=(15, 5))
_ = sns.lineplot(data=heart_zone_mins_df.melt(id_vars="date"),
                 x="date",
                 y="value",
                 hue="heart_zone_id")

# %%
skip_cell = True
# %%
if not skip_cell:
    df_list = list()
    for file in glob("data/MyFitbitData/Physical Activity/heart_rate*.json"):
        tmp_df = pd.read_json(file)
        df_list.append(pd.concat([pd.DataFrame(tmp_df.loc[x, "value"], index=[x]) for x in range(0, tmp_df.shape[0])])
        .mean()
        .to_frame()
        .T
        .assign(**{"date": pd.to_datetime(tmp_df["dateTime"]).dt.date.iloc[0]}))

    average_bpm_df = (pd.concat(df_list)
                    .sort_values(by="date")
                    .set_index("date")
                    .reset_index()
                    .drop_duplicates("date"))
    average_bpm_df.to_csv("data/MyFitbitData/Physical Activity/average_bpm_15-12-2022.csv")

# %%
daily_steps_df = (pd.concat([pd.read_json(file)
 .assign(**{"date": lambda d: pd.to_datetime(d["dateTime"]).dt.date})
 .drop("dateTime", axis=1)
 .groupby("date")
 .sum()
 .reset_index() for file in glob("data/MyFitbitData/Physical Activity/steps*.json")])
 .sort_values(by="date")
 .groupby("date")
 .sum()
 .reset_index())

# %%
daily_altitude_df = (pd.concat([pd.read_json(file)
 .assign(**{"date": lambda d: pd.to_datetime(d["dateTime"]).dt.date})
 .drop("dateTime", axis=1)
 .groupby("date")
 .sum()
 .reset_index() for file in glob("data/MyFitbitData/Physical Activity/altitude*.json")])
 .sort_values(by="date")
 .groupby("date")
 .sum()
 .reset_index())
# %%
daily_calories_df = (pd.concat([pd.read_json(file)
 .assign(**{"date": lambda d: pd.to_datetime(d["dateTime"]).dt.date})
 .drop("dateTime", axis=1)
 .groupby("date")
 .sum()
 .reset_index() for file in glob("data/MyFitbitData/Physical Activity/calories*.json")])
 .sort_values(by="date")
 .groupby("date")
 .sum()
 .reset_index())
# %%
daily_distance_df = (pd.concat([pd.read_json(file)
 .assign(**{"date": lambda d: pd.to_datetime(d["dateTime"]).dt.date})
 .drop("dateTime", axis=1)
 .groupby("date")
 .sum()
 .reset_index() for file in glob("data/MyFitbitData/Physical Activity/distance*.json")])
 .sort_values(by="date")
 .groupby("date")
 .sum()
 .reset_index()
 .assign(**{"distances": lambda d: (d["value"]/100_000).round(2)})
 .drop("value", axis=1)
 )
daily_distance_df.head()

# %%
lightly_zone_df = (pd.concat([pd.read_json(file)
 .assign(**{"date": lambda d: pd.to_datetime(d["dateTime"]).dt.date})
 .drop("dateTime", axis=1)
 .groupby("date")
 .sum()
 .reset_index() for file in glob("data/MyFitbitData/Physical Activity/lightly*.json")])
 .sort_values(by="date")
 .groupby("date")
 .sum()
 .reset_index())
lightly_zone_df.head()

# %%
very_zone_df = (pd.concat([pd.read_json(file)
 .assign(**{"date": lambda d: pd.to_datetime(d["dateTime"]).dt.date})
 .drop("dateTime", axis=1)
 .groupby("date")
 .sum()
 .reset_index() for file in glob("data/MyFitbitData/Physical Activity/very*.json")])
 .sort_values(by="date")
 .groupby("date")
 .sum()
 .reset_index())
very_zone_df.head()

# %%
fairly_zone_df = (pd.concat([pd.read_json(file)
 .assign(**{"date": lambda d: pd.to_datetime(d["dateTime"]).dt.date})
 .drop("dateTime", axis=1)
 .groupby("date")
 .sum()
 .reset_index() for file in glob("data/MyFitbitData/Physical Activity/moderately*.json")])
 .sort_values(by="date")
 .groupby("date")
 .sum()
 .reset_index())
fairly_zone_df.head()

# %%
sedentary_zone_df = (pd.concat([pd.read_json(file)
 .assign(**{"date": lambda d: pd.to_datetime(d["dateTime"]).dt.date})
 .drop("dateTime", axis=1)
 .groupby("date")
 .sum()
 .reset_index() for file in glob("data/MyFitbitData/Physical Activity/sedentary*.json")])
 .sort_values(by="date")
 .groupby("date")
 .sum()
 .reset_index())
sedentary_zone_df.head()

# %%
# SLEEP
daily_sleep_heart_df = (pd.concat([pd.read_csv(file) for file in glob("data/MyFitbitData/Sleep/Daily Heart*.csv")])
 .assign(**{"date": lambda d: pd.to_datetime(d["timestamp"]).dt.date})
 .drop("timestamp", axis=1)
 .sort_values("date")
 .set_index("date")
 .reset_index()
 )
# %%
daily_sleep_resp_df = (pd.concat([pd.read_csv(file) for file in glob("data/MyFitbitData/Sleep/Daily Respiratory*.csv")])
 .assign(**{"date": lambda d: pd.to_datetime(d["timestamp"]).dt.date})
 .drop("timestamp", axis=1)
 .sort_values("date")
 .set_index("date")
 .reset_index()
 )

# %%
daily_sleep_df = (pd.concat([pd.read_json(file) for file in glob("data/MyFitbitData/Sleep/sleep*.json")])
 .assign(**{"dateOfSleep": lambda d: pd.to_datetime(d["dateOfSleep"]).dt.date})
#  .drop("timestamp", axis=1)
#  .sort_values("date")
#  .set_index("date")
#  .reset_index()
 )

# %%
daily_SpO2_resp_df = (pd.concat([pd.read_csv(file) for file in glob("data/MyFitbitData/Sleep/Daily SpO2*.csv")])
 .assign(**{"date": lambda d: pd.to_datetime(d["timestamp"]).dt.date})
 .drop("timestamp", axis=1)
 .sort_values("date")
 .set_index("date")
 .reset_index()
 )
daily_SpO2_resp_df
# %%
computed_temp_df = (pd.concat([pd.read_csv(file) for file in glob("data/MyFitbitData/Sleep/Computed*.csv")])
 .astype({"sleep_start": np.datetime64,
          "sleep_end": np.datetime64})
 .sort_values(by="sleep_start")
 )

# %%
# pd.read_json(glob("data/MyFitbitData/Sleep/sleep*.json")[0])
# %%
# STRESS
stress_df = (pd.read_csv(glob("data/MyFitbitData/Stress/Stress*.csv")[0])
 .assign(**{"date": lambda d: pd.to_datetime(d["DATE"]).dt.date})
 .drop(["DATE", "UPDATED_AT"], axis=1)
 .sort_values(by="date")
 .set_index("date").reset_index()
 )
# %%
activity_df.head()
# %%
# daily_calories_df[daily_calories_df["date"]==pd.to_datetime("2022-09-11")]
# heart_zone_mins_df[heart_zone_mins_df["date"]==pd.to_datetime("2022-09-11")]
# lightly_zone_df[lightly_zone_df["date"]==pd.to_datetime("2022-09-11")]
# very_zone_df[very_zone_df["date"]==pd.to_datetime("2022-09-11")]
# fairly_zone_df[fairly_zone_df["date"]==pd.to_datetime("2022-09-11")]
# sedentary_zone_df[sedentary_zone_df["date"]==pd.to_datetime("2022-09-11")]

# %%
df = daily_calories_df.rename(columns={"value": "caloriesOut"}).merge(
    daily_steps_df.rename(columns={"value": "steps"})
    ).merge(
    lightly_zone_df.rename(columns={"value": "lightlyActiveMinutes"})
    ).merge(
    very_zone_df.rename(columns={"value": "veryActiveMinutes"})
    ).merge(
    fairly_zone_df.rename(columns={"value": "fairlyActiveMinutes"})
    ).merge(
    sedentary_zone_df.rename(columns={"value": "sedentaryMinutes"})
    ).merge(
    daily_distance_df
    ).astype({"date":"str"})

# %%
sleep_daily_column_list = [
    "minutesAfterWakeup",
    "efficiency",
    "minutesAwake",
    "duration",
    "minutesAsleep",
    "timeInBed",
    "dateOfSleep",
    "endTime",
    "startTime",
]
df = (daily_sleep_df[sleep_daily_column_list]
      .astype({"dateOfSleep":"str"})
      .assign(**{"duration": lambda d: d["duration"] / 60_000}))
    
# %%
db = deta.Base("fitbit_sleep_daily")
# %%
# _ = [db.insert(data=row_to_insert) for row_to_insert in df.to_dict(orient="records")]
# # %%
# for item in db.fetch().items:
#     db.delete(item["key"])
# %%
df.head()
# %%
daily_sleep_heart_df.head()
# %%
set(sleep_df.columns) - set(daily_sleep_df.columns), set(daily_sleep_df.columns) - set(sleep_df.columns)
# %%
sleep_df.head(1)

# %%
stress_df
# %%
