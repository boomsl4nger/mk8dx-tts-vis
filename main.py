import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import seaborn as sns
from typing import Literal

from outreach import fetch_wrs
from timeformat import TrackTime

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 0)
sns.set_theme(style="whitegrid")

STANDARDS_150 = pd.read_csv("data/150cc_standards.csv")
STANDARDS_200 = None

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

def update_wr_csv():
    pass

def determine_standard_and_diff(track_no: int, time: TrackTime, 
    standards: DataFrame | None = None) -> tuple[str, TrackTime]:
    """Calculate which Standard (rank) a given time falls in based on the given cut-off times. For
    Mario Kart, standards are usually something like:
    `God > Myth > Titan > Hero > Exp > Adv > Int > Beg`
    with subdivisions like `A > B > C`.

    Args:
        track_no (int): the track number for the given time.
        time (TrackTime): the given time to categorise.
        standards (DataFrame, optional): the cut-offs to determine the rank, defaults to default
        150cc standards.

    Returns:
        tuple[str, TrackTime]: tuple containing the rank name and the difference to the next rank
    """
    if standards is None: # Check if using custom standards
        standards = STANDARDS_150

    row = standards.iloc[track_no]
    for i, item in enumerate(row[1:].items()):
        rank, cutoff = item
        if time <= cutoff:
            # Get the previous bound if not already top rank
            to_next = row.get(i) if i > 0 else None
            return (rank, time - TrackTime(to_next)) if to_next else (rank, TrackTime("0:00.000"))
    return "Unranked", time - TrackTime(row.iloc[-1])

def create_timesheet_df(pbs: DataFrame, wrs: DataFrame, standards: DataFrame | None = None) -> DataFrame:
    """Create a timesheet with various data based on the given times and WRs. Standards can be 
    optionally included if desired, otherwise data will be only based on WR comparisons.
    
    Timesheet will contain:
    - TrackNo: track number (1-96)
    - Track: track name
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
        standard, stnd_diff = determine_standard_and_diff(track_no, time)
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
    valid = ["TimeNum", "StandardDiffNum", "WRNum", "WRDiffNum", "WRDiffNorm"]
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

def calculate_sheet_stats(timesheet: DataFrame, verbose: bool = False) -> Series:
    """Calculates various statistics for a given timesheet, such as for the WRDiff column.

    Args:
        timesheet (DataFrame): The timesheet.
        verbose (bool, optional): If true, prints results. Defaults to False.

    Returns:
        dict: The statistics of interest.
    """
    to_describe = ["WRDiffNum", "WRDiffNorm"]
    stats = timesheet[to_describe].describe()

    if verbose:
        print(stats)

    return stats

def create_visuals(timesheet: DataFrame):
    """Create some visualisations for a timesheet. Mainly for testing plots.

    Args:
        timesheet (DataFrame): Given timesheet.
    """
    sns.histplot(data=timesheet, x="WRDiffNum", binwidth=1.0, binrange=(2.0, 8.0))
    plt.show()

if __name__ in "__main__":
    # Create timesheet
    times_150 = pd.read_csv("data/150cc_times.csv")
    wrs_150 = pd.read_csv("data/150cc_wrs_12_01_2025.csv")
    timesheet = create_timesheet_df(times_150, wrs_150)

    # Do stuff with it
    # print(timesheet.head(10))
    basic_analysis(timesheet)
    # print(top_n_times(timesheet, col="WRDiffNorm", n=15, bottom=False))
    # calculate_sheet_stats(timesheet)
    # create_visuals(timesheet)