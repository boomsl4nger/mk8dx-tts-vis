from flask import Flask, flash, redirect, render_template, request, url_for
from markupsafe import escape
import numpy as np
import pandas as pd

import db
from timesheet import CC_CATEGORIES, ITEM_OPTIONS, STANDARDS_NAMES, STANDARDS_150, create_timesheet_df, calculate_sheet_stats

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
    overall_stats = calculate_sheet_stats(times_df)

    # Make arguments for chart generation
    diff_interval = 1
    wr_diff_values = times_df["WRDiffNum"].dropna()
    wr_bins = np.arange(0, max(wr_diff_values) + 1, diff_interval)  # 1-second intervals
    wr_hist, wr_bin_edges = np.histogram(wr_diff_values, bins=wr_bins)

    chart_diff_args = {
        "Labels": [f"{int(edge)}-{int(edge + 1)}" for edge in wr_bin_edges[:-1]],
        "Counts": wr_hist.tolist(),
    }

    rank_counts = {rank: 0 for rank in STANDARDS_NAMES}
    unique_ranks, rank_frequencies = np.unique(times_df["Standard"].dropna(), return_counts=True)
    for rank, count in zip(unique_ranks, rank_frequencies):
        if rank in rank_counts:
            rank_counts[rank] = count

    chart_rank_args = {
        "Labels": STANDARDS_NAMES,
        "Counts": [rank_counts[rank] for rank in STANDARDS_NAMES],
    }

    print(chart_diff_args)

    return render_template("timesheet.html",
        times=times_df.to_dict(orient="records"),
        overall_stats=overall_stats,
        chart_diff_args=chart_diff_args, chart_rank_args=chart_rank_args,
        selected_cc=selected_cc, selected_items=selected_items,
        cc_categories=CC_CATEGORIES, item_options=ITEM_OPTIONS)

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