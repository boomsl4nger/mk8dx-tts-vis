import numpy as np
import pandas as pd
from pandas import DataFrame

from TrackTime import TrackTime
from timesheet import CC_CATEGORIES, ITEM_OPTIONS, determine_wrs

rng = np.random.default_rng(0)
TRACK_NAMES = [row for row in pd.read_csv("data/track_names.csv", header=None).iloc[:, 3]]

def create_dummy_list(cc: str, items: str) -> list:
    """Creates a list of dummy track times (and improvements) for a given CC and item type.

    Rows are in the format: `(track, time_str, cc, items)`.

    Args:
        cc (str): CC.
        items (str): Item type.

    Returns:
        list: List of dummy time records.
    """
    if cc not in CC_CATEGORIES or items not in ITEM_OPTIONS:
        raise ValueError(f"Invalid args: {cc}, {items}")

    low, high = 5, 15

    wrs = [TrackTime(wr).get_seconds() for wr in determine_wrs(cc, "Shrooms")] # Assuming nita wrs don't exist
    if items == "NITA":
        wrs = [wr + 5 for wr in wrs] # Offset to account for shrooms roughly
    
    dummy = []
    for num, track in enumerate(TRACK_NAMES):
        wr = wrs[num]
        diff = max(0.5, rng.normal(7, 2)) # Normal dist for initial wr diff
        num_times = rng.integers(low, high) # Rand int for number of improvements
        for i in range(num_times):
            diff += max(0.1, rng.exponential(1)) # Exponential distribution for diffs
            time = wr + diff
            row = [track, TrackTime._format_seconds(time), cc, items]
            dummy.append(row)

    return dummy
        
def create_dummy_csv_all(save_file: bool = False, filename: str = None) -> DataFrame:
    """Convenience function for creating dummy data for each category combination.

    Args:
        save_file (bool, optional): If true, saves the CSV with the given filename. Defaults to False.
        filename (str, optional): Filename to use when saving. Defaults to `data/times_dummy_data.csv`.

    Returns:
        DataFrame: The fully combined dummy records df.
    """
    dummy = []
    for cc in CC_CATEGORIES:
        for item in ITEM_OPTIONS:
            dummy.extend(create_dummy_list(cc, item))

    df = DataFrame(dummy)
    
    if save_file:
        filename = filename if filename is not None else "data/times_dummy_data.csv"
        df.to_csv(filename, header=False, index=False)

    return df

if __name__ in "__main__":
    create_dummy_csv_all(save_file=True)