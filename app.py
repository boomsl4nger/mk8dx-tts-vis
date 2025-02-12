from flask import Flask, flash, redirect, render_template, request, url_for
from markupsafe import escape
import pandas as pd

import db
from timesheet import CC_CATEGORIES, ITEM_OPTIONS, STANDARDS_150, create_timesheet_df

app = Flask(__name__)

TRACKS = [(row["tr_name"], row["tr_abbrev"]) for row in db.get_tracks()]
TRACK_NAMES = [i[0] for i in TRACKS]

# Ideally WRs are scraped from the site on demand, but this is easier for now
wrs_150_shrooms = pd.read_csv("data/150cc_wrs_03_02_2025.csv", header=None)[1].values
wrs_200_shrooms = pd.read_csv("data/200cc_wrs_03_02_2025.csv", header=None)[1].values

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/timesheet", methods=["GET"])
def timesheet():
    selected_cc = request.args.get("cc", "150cc")
    selected_items = request.args.get("items", "Shrooms")

    # Fetch filtered data and create timesheet df
    pbs = [row["time_str"] for row in db.get_best_times(selected_cc, selected_items)]
    wrs = wrs_150_shrooms if selected_cc == "150cc" else wrs_200_shrooms
    times_df = create_timesheet_df(TRACK_NAMES, pbs, wrs, STANDARDS_150)

    return render_template("timesheet.html",
        times=times_df.to_dict(orient="records"),
        selected_cc=selected_cc,
        selected_items=selected_items,
        cc_categories=CC_CATEGORIES, 
        item_options=ITEM_OPTIONS)

@app.route("/update", methods=["GET", "POST"])
def update():
    error = None
    success = False

    if request.method == "POST":
        track = request.form["track"]
        time = request.form["time"]
        cc = request.form["cc"]
        items = request.form["items"]

        if track not in TRACK_NAMES: # Validate track exists
            error = "Track name not recognised."
        else:
            success = db.insert_time(track, time, cc, items)
            if not success: # Validate non-duplicate
                error = "Time already exists."
            else:
                success = True

    recent_times = db.get_recent_times("10")

    return render_template("update.html",
        track_names=TRACKS, cc_categories=CC_CATEGORIES, item_options=ITEM_OPTIONS,
        recent_times=recent_times,
        error=error, success=success)

@app.route("/picker")
def picker():
    return render_template("picker.html")

@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_time(entry_id):
    db.delete_time(entry_id)
    return redirect(url_for("update", deleted="true"))

if __name__ == "__main__":
    app.run(debug=True)