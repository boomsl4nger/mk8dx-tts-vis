from flask import Flask, redirect, render_template, request, url_for
from markupsafe import escape
import pandas as pd

import db
from timesheet import CC_CATEGORIES, ITEM_OPTIONS, create_timesheet_df

app = Flask(__name__)

# Ideally WRs are scraped from the site on demand, but this is easier for now
wrs_150_shrooms = pd.read_csv("data/150cc_wrs_03_02_2025.csv", header=None)
wrs_200_shrooms = pd.read_csv("data/200cc_wrs_03_02_2025.csv", header=None)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/timesheet", methods=["GET"])
def timesheet():
    # Get selected filters (default: 150cc, Shrooms)
    selected_cc = request.args.get("cc", "150cc")
    selected_items = request.args.get("items", "Shrooms")

    # Fetch filtered data
    best_times = pd.DataFrame([(row["track"], row["time_str"]) for row in db.get_best_times(selected_cc, selected_items)])
    wrs_df = wrs_150_shrooms if selected_cc == "150cc" else wrs_200_shrooms
    times_df = create_timesheet_df(best_times, wrs_df)

    return render_template(
        "timesheet.html",
        times=times_df.to_html(index=False, classes="table table-striped"),
        selected_cc=selected_cc,
        selected_items=selected_items,
        cc_categories=CC_CATEGORIES, 
        item_options=ITEM_OPTIONS
    )

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        track = request.form["track"]
        time = request.form["time"]
        cc = request.form["cc"]
        items = request.form["items"]
        db.insert_time(track, time, cc, items)

    track_names = [row[3] for row in db.get_tracks()]
    return render_template("update.html", track_names=track_names, cc_categories=CC_CATEGORIES, item_options=ITEM_OPTIONS)

@app.route("/picker")
def picker():
    return render_template("picker.html")

if __name__ == "__main__":
    app.run(debug=True)