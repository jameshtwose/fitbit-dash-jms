import os
from glob import glob
from deta import Deta
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.fitbit import make_fitbit_blueprint, fitbit
from datetime import date, timedelta
import pandas as pd

_ = load_dotenv()
app = Flask(__name__)
client_id = os.getenv("FITBIT_CLIENT_ID")
client_secret = os.getenv("FITBIT_CLIENT_SECRET")
app.secret_key = os.getenv("secret_key")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

# # remove all of the local versions of the latest csvs
# for file in glob("backend/data/*"):
#     os.remove(file)


FITBIT_SCOPES = [
    "activity",
    # "heartrate",
    # "location",
    # "nutrition",
    "profile",
    # "settings",
    "sleep",
    # "social",
    # "weight",
]

# read in the latest data saved in the Deta NOSQL
# mainly to get the necessary date range
deta = Deta(os.environ["health_deta_project_key"])
activity_daily_db = deta.Base("fitbit_activity_daily")
activity_daily_df = pd.DataFrame(activity_daily_db.fetch().items).assign(
    **{"date": lambda d: pd.to_datetime(d["date"])}
)

blueprint = make_fitbit_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    redirect_url="http://127.0.0.1:5000/login/fitbit/authorized/",
    # reprompt_consent=True,
    scope=FITBIT_SCOPES,
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    fitbit_data = None
    # start_date = activity_daily_df["date"].dt.date.max()
    start_date = date.today() - timedelta(days=2)
    end_date = date.today() - timedelta(days=1)
    # lookback_period = 60  # days
    user_info_endpoint = ""

    date_range = pd.date_range(start=start_date, end=end_date).date
    if fitbit.authorized:
        user_info_endpoint = "1/user/-/profile.json"
        fitbit_data = fitbit.get(user_info_endpoint).json()["user"]

        # GENERAL ACTIVITY
        user_info_endpoint = "1/user/-/activities.json"
        general_activity_data = fitbit.get(user_info_endpoint).json()
        pd.DataFrame(general_activity_data["best"]).to_csv("backend/data/activity_best.csv")
        pd.DataFrame(general_activity_data["lifetime"]).to_csv(
            "backend/data/activity_lifetime.csv"
        )

        # DAILY ACTIVITY
        activities_df = pd.DataFrame()
        for chosen_date in date_range:
            print(str(chosen_date))
            user_info_endpoint = f"1/user/-/activities/date/{str(chosen_date)}.json"
            fitbit_data = fitbit.get(user_info_endpoint).json()["summary"]
            current_df = pd.DataFrame(fitbit_data).head(1).assign(**{"date": str(chosen_date)})
            activities_df = pd.concat([activities_df, current_df])
        activities_df.to_csv(
            f"""backend/data/activity_{str(start_date)}_{str(end_date)}.csv"""
        )

        # DAILY SLEEP
        sleep_df = pd.DataFrame()
        for chosen_date in date_range:
            print(str(chosen_date))
            user_info_endpoint = f"""1.2/user/-/sleep/list.json?afterDate={str(chosen_date)}
            &sort=asc&offset=0&limit=1"""
            fitbit_data = fitbit.get(user_info_endpoint).json()["sleep"][0]
            current_df = pd.DataFrame(fitbit_data)
            sleep_df = pd.concat([sleep_df, current_df])
        sleep_df.to_csv(
            f"""backend/data/sleep_{str(start_date)}_{str(end_date)}.csv"""
        )

    return render_template(
        "index.j2", fitbit_data=fitbit_data, fetch_url=fitbit.base_url + user_info_endpoint
    )


@app.route("/login")
def login():
    return redirect(url_for("fitbit.login"))


if __name__ == "__main__":
    app.run(debug=True)

# https://github.com/lila/flask-dance-fitbit/blob/main/fitbit.py
