import pandas as pd
from ast import literal_eval

activity_daily_column_list = [
    "date",
    "caloriesOut",
    "distances",
    "steps",
    "activityCalories",
    "marginalCalories",
    "sedentaryMinutes",
    "lightlyActiveMinutes",
    "fairlyActiveMinutes",
    "veryActiveMinutes",
]

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


def dict_to_df(col):
    df = pd.DataFrame(literal_eval(col[0]), index=[0])
    df.columns = [f"{col.name}_{x}" for x in df.columns.tolist()]
    return df


def insert_values(db, data):
    _ = [db.insert(data=row_to_insert) for row_to_insert in data.to_dict(orient="records")]


def delete_values(db):
    for item in db.fetch().items:
        db.delete(item["key"])

