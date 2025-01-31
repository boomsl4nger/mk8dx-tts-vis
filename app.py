from flask import Flask, render_template
from markupsafe import escape
import pandas as pd

from timesheet import create_timesheet_df

app = Flask(__name__)

# Create timesheet
times_150 = pd.read_csv("data/150cc_times.csv", header=None)
wrs_150 = pd.read_csv("data/150cc_wrs_23_01_2025.csv", header=None)
timesheet_df = create_timesheet_df(times_150, wrs_150)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/timesheet")
def timesheet():
    return render_template("timesheet.html", tables=[timesheet_df.to_html(classes="table table-striped", index=False)], titles=timesheet_df.columns.values)

if __name__ == "__main__":
    app.run(debug=True)