import pandas as pd
import numpy as np
from deta import Deta
from dotenv import load_dotenv, find_dotenv
import os


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
    return df
