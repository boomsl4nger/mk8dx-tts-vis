DROP TABLE IF EXISTS tracks;
DROP TABLE IF EXISTS track_times;

CREATE TABLE tracks (
    tr_number INTEGER PRIMARY KEY,
    cup TEXT NOT NULL,
    cup_type TEXT NOT NULL,
    tr_name TEXT UNIQUE NOT NULL,
    tr_abbrev TEXT UNIQUE NOT NULL
);

CREATE TABLE track_times (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track TEXT NOT NULL,
    time_str TEXT NOT NULL,
    time_sec REAL NOT NULL,
    cc TEXT NOT NULL,
    items TEXT NOT NULL,
    FOREIGN KEY (track) REFERENCES tracks(tr_name)
);
