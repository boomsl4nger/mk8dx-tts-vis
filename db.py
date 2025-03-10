import csv
import sqlite3
from sqlite3 import Connection

from timesheet import CC_CATEGORIES, ITEM_OPTIONS
from TrackTime import TrackTime

DB_FILE = "track_times.db"

def get_db() -> Connection:
    """Get the db connection.

    See: https://flask.palletsprojects.com/en/stable/patterns/sqlite3/

    Returns:
        Connection: Connection object.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def close_db(conn: Connection):
    """Close the db connection.

    Args:
        conn (Connection): Connection object.
    """
    conn.close()

def query_db(query: str, args: tuple = (), one: bool = False) -> tuple:
    """Function for interacting with the db given a query and optional arguments.

    Args:
        query (str): Query to execute.
        args (tuple, optional): Query arguments. Defaults to ().
        one (bool, optional): If true, returns first result. Defaults to False.

    Returns:
        tuple: Result of the query.
    """
    conn = get_db()
    cur = conn.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    close_db(conn)
    return (rows[0] if rows else None) if one else rows

def init_db():
    """Initialise the db based on the schema file."""
    conn = get_db()
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    close_db(conn)

def init_tracks_from_csv(path: str):
    """Insert track information into the table given a CSV file path.

    Args:
        path (str): Path to the CSV file.
    """
    conn = get_db()
    with open(path) as f:
        r = csv.reader(f)
        tracks = [tuple(row) for row in r]
        conn.executemany(
            "INSERT INTO tracks (tr_number, cup, cup_type, tr_name, tr_abbrev) VALUES (?, ?, ?, ?, ?)", 
            tracks
        )
    conn.commit()
    close_db(conn)

def init_times_from_csv(path: str, cc: str = "150cc", items: str = "Shrooms"):
    """Insert some preset times into the time table in the db given a CSV file path.

    The CSV file should have rows in the following format: `track_name, time_str`.
    For example: `Mario Kart Stadium, 1:40.000`

    Args:
        path (str): CSV file path.
        cc (str, optional): CC. Defaults to "150cc".
        items (str, optional): Item type. Defaults to "Shrooms".
    """
    if cc not in CC_CATEGORIES or items not in ITEM_OPTIONS:
        raise ValueError(f"Invalid CC or item type: {cc} | {items}")
    
    conn = get_db()
    with open(path) as f:
        r = csv.reader(f)
        times = [(row[0], row[1], TrackTime(row[1]).get_seconds(), cc, items) for row in r]
        conn.executemany(
            "INSERT INTO track_times (track, time_str, time_sec, cc, items) VALUES (?, ?, ?, ?, ?)", 
            times
        )
    conn.commit()
    close_db(conn)

def init_dummy_times(path: str):
    """Insert randomly generated dummy times into the db given a CSV file path.

    Args:
        path (str): CSV file path.
    """
    conn = get_db()
    with open(path) as f:
        r = csv.reader(f)
        times = [(row[0], row[1], TrackTime(row[1]).get_seconds(), row[2], row[3]) for row in r]
        conn.executemany(
            "INSERT INTO track_times (track, time_str, time_sec, cc, items) VALUES (?, ?, ?, ?, ?)", 
            times
        )
    conn.commit()
    close_db(conn)

def insert_time(track: str, time: str, cc: str, items: str):
    """Insert a time in to the times table in the db. Given time should be formatting as the typical
    `M:SS.sss` format, gets converted automatically by this function as necessary.

    Args:
        track (str): Full track name.
        time (str): Time in string format.
        cc (str): CC.
        items (str): Item type.
    """
    # Formatting the time
    time_sec = TrackTime(time).get_seconds()

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO track_times (track, time_str, time_sec, cc, items) VALUES (?, ?, ?, ?, ?)",
            (track, time, time_sec, cc, items),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        close_db(conn)
        return False
    
    close_db(conn)
    return True

def delete_time(id: str):
    """Deletes an entry from the times table given an ID.

    Args:
        id (str): ID of the entry.
    """
    conn = get_db()
    conn.execute("DELETE FROM track_times WHERE id = ?", (id,))
    conn.commit()
    close_db(conn)

#region Get queries
def get_tracks() -> tuple:
    """Get all rows from the tracks table in the db.

    Returns:
        tuple: Tuple containing Row objects.
    """
    return query_db("SELECT * FROM tracks ORDER BY tr_number")

def get_recent_times(n: str) -> tuple:
    """Gets the n most recent additions to the track_times table.

    Args:
        n (str): Number of entries to get.

    Returns:
        tuple: Tuple containing Row objects from the db.
    """
    query = """
        SELECT tt.id, tt.track, t.tr_abbrev, tt.time_str, tt.cc, tt.items
        FROM track_times tt
        JOIN tracks t ON tt.track = t.tr_name
        ORDER BY id DESC
        LIMIT ?
    """
    return query_db(query, (n,))

def get_best_times(cc: str, items: str) -> tuple:
    """Gets the current PBs from the times table in the db, for a given CC and item type. Query does
    a left outer join on the tracks table, so all tracks are included regardless of whether there
    are any respective saved times. Missing times are returned as NULL for `best_time_sec` and `"-"`
    for `time_str`.

    Args:
        cc (str): CC.
        items (str): Item type.

    Returns:
        tuple: Tuple containing Row objects from the db.
    """
    query = """
        SELECT t.tr_name AS track, 
            COALESCE(MIN(tt.time_sec), NULL) AS best_time_sec, 
            COALESCE(tt.time_str, '-') AS time_str
        FROM tracks t
        LEFT JOIN track_times tt 
            ON t.tr_name = tt.track 
            AND tt.cc = ? 
            AND tt.items = ?
        GROUP BY t.tr_name
        ORDER BY t.tr_number
    """
    return query_db(query, (cc, items))

def get_times_for_track(name: str, cc: str, items: str) -> tuple:
    """Gets the times for a given track combination.

    Args:
        name (str): Track name.
        cc (str): Speed.
        items (str): Item type.

    Returns:
        tuple: Tuple containing Row objects from the db.
    """
    query = """
        SELECT id, time_str, time_sec
        FROM track_times
        WHERE track = ? AND cc = ? and items = ?
        ORDER BY time_sec
    """
    return query_db(query, (name, cc, items))
#endregion

if __name__ in "__main__":
    # Caution: running this file directly will initialise the database
    tracks_path = "data/track_names.csv"
    dummy_times_path = "data/times_dummy_data.csv"
    times_path = "data/times_data_file_here"

    # Uncomment the following if you want to re-init the db and the tracks table
    init_db()
    print("DB initialised.")
    init_tracks_from_csv(tracks_path)
    print("Track table populated.")

    # These functions can be swapped to use dummy data or not
    init_dummy_times(dummy_times_path)
    # init_times_from_csv(times_path)
    print("Times table populated.")