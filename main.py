import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
import seaborn as sns
from typing import Literal

from outreach import fetch_wrs
from timeformat import TrackTime

sns.set_theme(style="whitegrid")

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

def basic_analysis(data: DataFrame):
    """Runs a basic analysis on the given df, printing the results.

    Args:
        data (DataFrame): df of interest.
    """
    print("First and last 5 rows:")
    print(data.head())
    print(data.tail())
    
    print("\nShape (rows, columns):")
    print(data.shape)
    
    # Display information about the dataset (columns, non-null values, dtypes)
    print("\nInfo about the dataset:")
    print(data.info())
    
    print("\nMissing values:")
    print(data.isnull().sum())

    print("\nDuplicates info:")
    dupes = data[data.duplicated()]
    print(f"Count: {dupes.shape}")
    print(dupes)
    
    print("\nDescriptive statistics:")
    print(data.describe())

def create_timesheet_df(pbs: list, wrs: list, standards: DataFrame):
    pass

if __name__ in "__main__":
    standards_150 = pd.read_csv("150cc_standards.csv")
    times_150 = pd.read_csv("150cc_times.csv")
    wrs_150 = fetch_wrs("150")
    timesheet = create_timesheet_df(times_150, wrs_150, standards_150)