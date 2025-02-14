import csv
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import seaborn as sns
from typing import Literal

from outreach import fetch_wrs_shrooms
from TrackTime import TrackTime, TrackTimeExt

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 0)
sns.set_theme(style="whitegrid")

#region Globals
CC_CATEGORIES = ["150cc", "200cc"]
ITEM_OPTIONS = ["Shrooms", "NITA"]

STANDARDS_150 = pd.read_csv("data/150cc_standards.csv")
STANDARDS_200 = None
STANDARDS_NAMES = [
    'God', 'Myth A', 'Myth B', 'Myth C', 'Titan A', 'Titan B', 'Titan C', 
    'Hero A', 'Hero B', 'Hero C', 'Exp A', 'Exp B', 'Exp C', 'Adv A', 'Adv B', 'Adv C', 
    'Int A', 'Int B', 'Int C', 'Beg A', 'Beg B', 'Beg C'
]

# See: https://matplotlib.org/stable/gallery/color/colormap_reference.html
cmap = matplotlib.colormaps.get_cmap("plasma")
gradient = np.linspace(0, 1, len(STANDARDS_NAMES))
STANDARDS_COLOURS = [matplotlib.colors.to_hex(cmap(i)) for i in gradient]
#endregion

#region File functions
def raw_to_csv(input_filename: str, output_filename: str):
    """Converts a text file with track times to CSV. Text file format should be tab separated, such
    as `track_name \\t track_time`.

    Args:
        input_text (str): Filename of the raw text file.
        output_filename (str): Filename to be saved to.
    """
    with open(input_filename) as f:
        lines = f.read().strip().split("\n")

    with open(output_filename, mode="w", newline="", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['Track', 'Time'])

        for line in lines:
            track, time = line.rsplit('\t', 1)  # Split on the last tab character
            csv_writer.writerow([track, time])

def clean_standards(filename: str):
    """Specialised to clean the raw CSV download from original Google Sheets page.

    Args:
        filename (str): Filename.
    """
    df = pd.read_csv(filename)
    df.drop(["Cup", "WR", "-"], axis=1, inplace=True)
    df.to_csv(filename, index=False)

def basic_analysis(data: DataFrame, verbose: bool = False):
    """Runs a basic analysis on the given df, printing the results.

    Args:
        data (DataFrame): df of interest
        verbose (bool): if true, prints more information about the df
    """
    print("First and last 5 rows:")
    print(data.head())
    print()
    print(data.tail())
    
    print("\nShape (rows, columns):")
    print(data.shape)
    
    if verbose:
        # Display information about the dataset (columns, non-null values, dtypes)
        print("\nInfo about the dataset:")
        print(data.info())
        
        print("\nMissing values:")
        print(data.isnull().sum())

        # print("\nDuplicates info:")
        # dupes = data[data.duplicated()]
        # print(f"Count: {dupes.shape}")
        # print(dupes)
        
        print("\nDescriptive statistics:")
        print(data.describe())

def update_wr_csv(cc: Literal["150cc", "200cc"] = "150cc", path: str = None):
    """Updates the current WR CSV file by pulling the latest times and saving to a new file. If no
    filename is given, creates one by default with the format:
    - `[cc]_wrs_[DD_MM_YYYY].csv`

    Useful reference: https://strftime.org/

    Args:
        cc (str, optional): CC for WRs. Defaults to 150cc.
        path (str, optional): File path to use when writing. Defaults to None.
    """
    if path is None:
        date_part = datetime.now().strftime("%d_%m_%Y")
        path = f"data/{cc}_wrs_{date_part}.csv"

    times = DataFrame(fetch_wrs_shrooms(cc))
    times.to_csv(path, header=False, index=False)
#endregion

#region Timesheet functions
def calculate_standard(time: TrackTime, standards: list, names: list | None = None) -> tuple:
    """Calculate which Standard (rank) a given time falls in based on the given cut-off times. For
    Mario Kart, standards are usually something like:
    `God > Myth > Titan > Hero > Exp > Adv > Int > Beg`
    with subdivisions like `A > B > C`.

    As an example, if the time was `1:00.000` and the standards were `Gold: 0:55.000` and 
    `Silver: 1:05.000`, then the time would be classified as Silver with a difference of `0:05.000`
    to the next standard.

    Args:
        time (TrackTime): The given time to categorise.
        standards (list): The cut-offs to determine the rank. E.g. `["1:00.000", "1:10.000"]`
        names (list): The names of the standards. E.g. `["Gold", "Silver"]`

    Returns:
        tuple: Tuple containing (rank_arg, rank_name, next_rank_diff).
    """
    if names is None:
        names = STANDARDS_NAMES

    if len(standards) != len(names):
        raise ValueError("Standard names and cutoffs are different lengths.")

    for i, cutoff in enumerate(standards):
        if time <= cutoff:
            # Get the previous bound if not already top rank
            rank = names[i]
            to_next = standards[i-1] if i > 0 else None
            diff = time - TrackTime(to_next) if to_next else TrackTime("0:00.000")
            return i+1, rank, diff
    return len(names)+1, "Unranked", time - TrackTime(standards[-1])

def create_timesheet_df(tracks: list, pbs: list, wrs: list, standards: DataFrame | None = None) -> DataFrame:
    """Create a timesheet for the given PB times. The timesheet is a DataFrame that includes various 
    useful columns, such as the WR, standard, and differences. Columns appended with `"Num"` are 
    copies of another column with the time converted from a formatted string (M:SS.sss) to a float, 
    in seconds. StandardNum is different as this contains the number position of the rank, e.g.,
    `Gold` would be 1 if it was the top rank, etc.

    Note that the lists of track names and times are assumed to already be aligned.

    Args:
        tracks (list): Ordered list of track names.
        pbs (list): Ordered list of PBs.
        wrs (list): Ordered list of WRs.
        standards (DataFrame | None, optional): Standards used to determine the rank of each track time. Defaults to None.

    Raises:
        ValueError: If the standards are not provided. This will be changed in future.

    Returns:
        DataFrame: The completed timesheet.
    """
    # TODO support functionality when standards are not needed
    if standards is None:
        raise ValueError("Standards must be provided at this point.")

    column_names = [
        "TrackNo", "TrackName", "Time", "TimeNum",
        "Standard", "StandardNum", "StandardDiff", "StandardDiffNum",
        "WR", "WRNum", "WRDiff", "WRDiffNum", "WRDiffNorm"
    ]
    stnd_names = standards.columns[1:]
    
    timesheet = []
    for num in range(len(tracks)):
        tr_name = tracks[num]
        wr_time = TrackTime(wrs[num])

        try:
            TrackTime(pbs[num])
        except ValueError: # Time is not valid, and likely empty
            timesheet.append([
                num + 1, tr_name, "-", "-",
                "-", "-", "-", "-",
                wr_time, wr_time.get_seconds(), "-", "-", 0
            ])
            continue

        row = []
        pb_time = TrackTime(pbs[num])
        wr_diff = pb_time - wr_time

        # Calculate standards
        stnd_arg, stnd_name, stnd_diff = calculate_standard(pb_time, standards.iloc[num][1:], stnd_names)

        row = [
            num + 1, tr_name, pb_time, pb_time.get_seconds(),
            stnd_name, stnd_arg, stnd_diff, stnd_diff.get_seconds(),
            wr_time, wr_time.get_seconds(), wr_diff, wr_diff.get_seconds()
        ]
        row.append(round(row[-1] / row[-3] * 100, 5)) # WRDiffNorm
        timesheet.append(row)

    return DataFrame(timesheet, columns=column_names)

def create_timesheet_df_old(pbs: DataFrame, wrs: DataFrame, standards: DataFrame | None = None) -> DataFrame:
    """NOTE: this function is deprecated. Please see `create_timesheet_df` instead.
    
    Create a timesheet with various data based on the given times and WRs. Standards can be 
    optionally included if desired, otherwise data will be only based on WR comparisons.
    
    Timesheet will contain:
    - TrackNo: track number (1-96)
    - TrackName: track name
    - Time: given user time
    - Standard: rank name based on the given standard cut-offs
    - StandardDiff: difference between the next standard and the user time
    - WR: given world record
    - WRDiff: time - wr
    - WRDiffNorm: diff / wr * 100
    - [Name]Num: numerical version of TrackTime columns for plotting purposes

    Args:
        pbs (DataFrame): Some given times.
        wrs (DataFrame): WR times.
        standards (DataFrame, optional): Standards by which to categorise the given times. Defaults 
        to None.

    Returns:
        DataFrame: Filled timesheet.
    """
    col_names = ["TrackNo", "TrackName", "Time", "Standard", "StandardDiff",
                 "WR", "WRDiff", "WRDiffNorm",
                 "TimeNum", "StandardDiffNum", "WRNum", "WRDiffNum"]
    timesheet = []
    for track_no in range(len(pbs)):
        name, time = pbs.iloc[track_no]
        wr = wrs.iloc[track_no, 1]

        # Convert to TrackTime class to handle operations
        time = TrackTime(time)
        wr = TrackTime(wr)
        standard, stnd_diff = calculate_standard(track_no, time)
        wr_diff = time - wr

        timesheet.append([
            track_no + 1, name, time, standard, stnd_diff, wr, wr_diff, 
            wr_diff.get_seconds() / wr.get_seconds() * 100,
            time.get_seconds(), stnd_diff.get_seconds(), wr.get_seconds(), wr_diff.get_seconds()
        ])

    return DataFrame(timesheet, columns=col_names)

def check_col_numeric(name: str) -> bool:
    """Check if a given column name for a timesheet is numeric.

    Args:
        name (str): column name.

    Returns:
        bool: true if a valid name, otherwise false.
    """
    valid = ["TimeNum", "StandardNum", "StandardDiffNum", "WRNum", "WRDiffNum", "WRDiffNorm"]
    return name in valid

def top_n_times(timesheet: DataFrame, n: int = 10, bottom: bool = False, col: str = "TimeNum") -> DataFrame:
    """Sorts a given timesheet based on some criteria.

    Args:
        timesheet (DataFrame): The timesheet of interest.
        n (int, optional): Number of entries to show. Defaults to 10.
        bottom (bool, optional): If true, sort in descending order. Defaults to False.
        col (str, optional): Column name to sort by. Defaults to "TimeNum".

    Raises:
        ValueError: If column name is invalid.

    Returns:
        DataFrame: Sorted and reduced timesheet.
    """
    if not check_col_numeric(col):
        raise ValueError("Column name needs to be numeric to sort.")
    return timesheet.sort_values(by=col, ascending=(not bottom)).iloc[:n]

def calculate_sheet_stats(sheet: DataFrame, verbose: bool = False) -> dict:
    """Calculates various statistics for a given timesheet, such as for the WRDiff column.

    Args:
        sheet (DataFrame): The timesheet.
        verbose (bool, optional): If true, prints results. Defaults to False.

    Returns:
        dict: The statistics of interest.
    """
    # stats = sheet[["WRDiffNum", "WRDiffNorm"]].describe()
    # sheet.agg(["mean", "median", "std"])

    stats = {}

    # Total times
    stats["Total PB Time"] = TrackTimeExt._format_seconds(sheet["TimeNum"].sum())
    stats["Total WR Time"] = TrackTimeExt._format_seconds(sheet["WRNum"].sum())
    stats["Total Diff"] = TrackTimeExt._format_seconds(sheet["WRDiffNum"].sum())

    # Overall rank
    stnd_avg = sheet["StandardNum"].mean() - 0.5
    stats["Rank Num Average"] = f"{stnd_avg:.2f}"
    stats["Overall Rank"] = STANDARDS_NAMES[int(round(stnd_avg))]
    # TODO improve this metric

    # Other stats
    diff_avg = sheet["WRDiffNum"].mean()
    diff_med = sheet["WRDiffNum"].median()
    stats["Diff Average"] = (diff_avg, TrackTime._format_seconds(diff_avg))
    stats["Diff Median"] = (diff_med, TrackTime._format_seconds(diff_med))
    stats["Diff Std Dev"] = TrackTime._format_seconds(sheet["WRDiffNum"].std())

    if verbose:
        print(stats)

    return stats
#endregion

#region Data visualisation functions
def create_visuals_overall(timesheet: DataFrame):
    """Create some visualisations for a timesheet. Mainly for testing plots.

    For inspo: https://seaborn.pydata.org/examples/index.html

    Args:
        timesheet (DataFrame): Given timesheet.
    """
    # Histogram of WR diffs
    sns.histplot(data=timesheet, x="WRDiffNum", binwidth=1.0, binrange=(2.0, 8.0))
    plt.xlabel("WR Diff (s)")
    plt.ylabel("Count")
    plt.show()

    # Histogram of WR diffs normed
    sns.histplot(data=timesheet, x="WRDiffNorm", stat="percent")
    plt.xlabel("WR Diff Norm (%)")
    plt.ylabel("Percent")
    plt.show()

    # Bar chart of standard counts
    name_counts = {}
    for name in STANDARDS_NAMES:
        name_counts[name] = 0

    for name in timesheet["Standard"]:
        name_counts[name] += 1

    name_counts = Series(name_counts)
    print(name_counts.head(20))
    sns.barplot(data=name_counts, order=STANDARDS_NAMES, orient="y", palette="rocket")
    plt.xlabel("Count")
    # plt.ylabel("Standard Name")
    plt.show()

def create_visuals_track(timesheet: DataFrame, standards: DataFrame = STANDARDS_150, track_name: str = None, track_no: int = None):
    """Create visualisations for a given individual track. Also used for testing mostly. Either the
    track name or number must be provided.

    See: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axvspan.html
    See: https://seaborn.pydata.org/tutorial/properties.html

    Args:
        timesheet (DataFrame): The timesheet.
        track_name (str, optional): Track name.
        track_no (int, optional): Track number.
        standards (DataFrame, optional): Standards for all tracks. Defaults to 150 standards.
    """
    if track_name is None and track_no is None:
        raise ValueError("Need to give either a track name or number, e.g. Mario Kart Stadium (1).")

    # TODO support for track numbers, should infer track name from given number

    track_stats = timesheet.loc[timesheet["TrackName"] == track_name]
    time_pb = track_stats.loc[:, "Time"].iloc[0].get_seconds()
    time_wr = track_stats.loc[:, "WR"].iloc[0].get_seconds()

    track_stnds = standards.loc[standards["Track"] == track_name]
    track_stnds_secs = [TrackTime(i).get_seconds() for i in track_stnds.iloc[0, 1:]]

    # Plot the times as data points
    sns.stripplot(x=[time_pb, time_wr], jitter=False, marker="d", size=10, color="k")

    # Plot the standards as shaded vertical regions
    track_stnds_secs.extend(list(plt.xlim()))
    track_stnds_secs = sorted(track_stnds_secs)
    for i in range(len(track_stnds_secs) - 1):
        time_1, time_2 = track_stnds_secs[i:i+2]
        if time_1 > time_pb:
            plt.xlim(track_stnds_secs[0], time_1)
            break

        plt.axvspan(time_1, time_2, facecolor=STANDARDS_COLOURS[i], alpha=0.5)
        plt.text(x=np.mean((time_1, time_2)), y=plt.ylim()[0] - 0.05, s=STANDARDS_NAMES[i], horizontalalignment="center", verticalalignment="bottom", rotation=90) # Kerning here is fucking annoying, maybe x-value
    
    plt.xlabel("Time (s)")
    plt.ylabel(f"{track_name}")
    plt.show()
#endregion

if __name__ in "__main__":
    # Update WR CSVs
    # update_wr_csv("150")
    # update_wr_csv("200")

    # Create timesheet
    times_150 = pd.read_csv("data/150cc_times.csv", header=None)
    wrs_150 = pd.read_csv("data/150cc_wrs_03_02_2025.csv", header=None)
    track_names = times_150[0].values
    timesheet = create_timesheet_df(track_names, times_150[1].values, wrs_150[1].values, STANDARDS_150)

    # Testing standard diff calcs
    # print(calculate_standard("1:01.010", ["0:55.000", "1:01.000"], ["A", "B"]))

    # Do stuff with it
    # print(timesheet.head(10))
    # basic_analysis(timesheet)
    # print(top_n_times(timesheet, col="WRDiffNum", n=10, bottom=False))
    # calculate_sheet_stats(timesheet, verbose=True)
    # create_visuals_overall(timesheet)
    # create_visuals_track(timesheet, track_name="Mario Kart Stadium", standards=STANDARDS_150)