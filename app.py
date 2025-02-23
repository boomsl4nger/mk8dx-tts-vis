from flask import Flask, redirect, render_template, request, url_for
import numpy as np

import db
from timesheet import *

app = Flask(__name__)

TRACKS = [(row["tr_name"], row["tr_abbrev"]) for row in db.get_tracks()]
TRACK_NAMES = [i[0] for i in TRACKS]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/timesheet", methods=["GET"])
def timesheet():
    selected_cc = request.args.get("cc", "150cc")
    selected_items = request.args.get("items", "Shrooms")

    # Fetch filtered data and create timesheet df
    pbs = [row["time_str"] for row in db.get_best_times(selected_cc, selected_items)]
    wrs = determine_wrs(selected_cc, selected_items)
    times_df = create_timesheet_df(TRACK_NAMES, pbs, wrs, selected_cc, selected_items)
    overall_stats = calculate_sheet_stats(times_df)

    # Make arguments for chart generation
    diff_interval = 1
    wr_diff_values = times_df["WRDiffNum"].dropna()
    wr_bins = np.arange(0, max(wr_diff_values) + 1 if wr_diff_values.any() else 1, diff_interval)
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

    return render_template("timesheet.html",
        times=times_df.to_dict(orient="records"),
        overall_stats=overall_stats,
        chart_diff_args=chart_diff_args, chart_rank_args=chart_rank_args,
        selected_cc=selected_cc, selected_items=selected_items,
        cc_categories=CC_CATEGORIES, item_options=ITEM_OPTIONS)

@app.route("/update", methods=["GET"])
def update():
    return render_template("update.html",
        track_names=TRACKS, cc_categories=CC_CATEGORIES, item_options=ITEM_OPTIONS,
        recent_times=db.get_recent_times("10"))

@app.route("/track")
def track():
    track_name = request.args.get("track")
    selected_cc = request.args.get("cc", "150cc")
    selected_items = request.args.get("items", "Shrooms")

    if not track_name:
        raise ValueError(f"Track name is invalid: {track_name}")

    # Get more track info
    tr_num, tr_abbrev = db.query_db("SELECT tr_number, tr_abbrev FROM tracks WHERE tr_name = ?", (track_name,), one=True)

    # Determine the WR
    wr_df = determine_wrs(selected_cc, selected_items)
    wr_str = wr_df[tr_num] if wr_df is not None else None

    # Fetch PB times from db for specific combination
    times = db.get_times_for_track(track_name, selected_cc, selected_items)
    df = create_track_times_df([row["time_sec"] for row in times])
    df["RowId"] = [row["id"] for row in times]

    # Timesheet excerpt
    pb = times[0]["time_str"] if len(times) > 0 else None
    ts_excerpt = create_ts_excerpt_df(tr_num, track_name, pb, wr_str, selected_cc, selected_items)

    return render_template("track.html",
        track_name=track_name, track_abbrev=tr_abbrev,
        times=df.to_dict(orient="records"), wr=[wr_str, TrackTime(wr_str).get_seconds() if wr_str else None],
        ts_excerpt=ts_excerpt.to_dict(orient="records"),
        selected_cc=selected_cc, selected_items=selected_items,
        cc_categories=CC_CATEGORIES, item_options=ITEM_OPTIONS)

@app.route("/picker")
def picker():
    return render_template("picker.html")

@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_time(entry_id):
    # Extract query parameters before deleting the entry
    track_name = request.form.get("track_name")
    selected_cc = request.form.get("selected_cc", "150cc")
    selected_items = request.form.get("selected_items", "Shrooms")

    db.delete_time(entry_id)

    if track_name:
        return redirect(url_for("track", track=track_name, cc=selected_cc, items=selected_items, deleted="true"))
    return redirect(url_for("update", deleted="true"))

@app.route("/insert_time", methods=["POST"])
def insert_time():
    track = request.form.get("track")
    time = request.form.get("time")
    cc = request.form.get("cc", "150cc")
    items = request.form.get("items", "Shrooms")

    if not track or track not in TRACK_NAMES:   # Validate track exists
        error = "Track name not recognised."
    else:
        success = db.insert_time(track, time, cc, items)
        if not success:                         # Validate non-duplicate
            error = "Time already exists."
        else:
            success = True
            error = None

    referrer = request.referrer or url_for("update")
    if "track" in referrer:
        return redirect(url_for("track", track=track, cc=cc, items=items, success="true" if success else "false", error=error))
    return redirect(url_for("update", success="true" if success else "false", error=error))



if __name__ == "__main__":
    app.run(debug=True)