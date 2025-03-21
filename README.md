# Mario Kart 8 Deluxe Time Trials Visualiser

Personal project combining my hobby with some data visualisation and analysis.
This is mostly a practical way to try learn more data vis and web dev.
Currently, most of the core features I wanted are functional and decently user-friendly too.
I am generally quite happy with the overall state of the project considering it was just for fun/practice.

## High-level Goals
See `todo.md` for more specific items.
- [x] Back-end stuff like parsing and combining data, simple visualisations
- [x] Set up Flask for a basic web app
- [x] Set up SQLite for database, design schemas
- [x] Design pages for different features using Bootstrap
- [x] Front-end libraries for things like data tables, interactive graphs

## Overview
The application is built using Flask, which is run with the following command:
```
python -m flask run
```
The application should be running on [localhost:5000](http://127.0.0.1:5000/).
Append `--debug` to run in debug mode.

It is strongly recommended to be working in a virtual environment. This is made pretty simple by running the following commands:
```
python -m venv env          # to init
.\env\Scripts\activate      # Windows
source env/bin/activate     # MacOS / Linux
deactivate                  # to exit
```

### Requirements
Python can be downloaded [here](https://www.python.org/downloads/). To install the required dependencies (preferably in your venv), run the following command:
```
pip install -r requirements.txt
```

Updating the requirements file is very simple; the following command will generate a file with all the dependencies in the current environment:
```
pip freeze > requirements.txt
```

### Initialising the database
To initialise (or drop and re-create) the database file, run the `db.py` file:
```
python db.py
```
This will create the tables as specified in the `schema.sql` file, as well as populate the track table with the necessary info and the times table with some pre-generated dummy data. You can swap the commented lines in `db.py` to use your own data, but be sure to read what params are needed.
To regenerate the dummy times data, run
```
python generate_times.py
```

### Updating the WRs
There are functions to automatically fetch and update the WR CSV files. Currently, this only supports updating the shroom WRs because the website is easier to scrape. The function is in `timesheet.py` and requires a `cc` parameter, for example:
```
python -c "import timesheet as ts; ts.update_wr_csv('150cc')"
```

Note that currently NITA WRs and 200cc standards are not supported, so will appear as missing in the timesheet. The Shrooms WRs were last updated 25/02/2025; this isn't *fully* automated just yet, so best not to update the WRs unless you know what you're doing.

## Example Images
Below are some images of what the project currently looks like!

Timesheet example using dummy data:
![Timesheet snippet](images/ex_timesheet.png)

Overall statistics for the above timesheet:
![Overall statistics](images/ex_overall_stats.png)

Individual track page for Tour Madrid Drive (150cc, Shrooms):
![Individual track stats](images/ex_indiv_track_bands.png)

## License & References
I'm making this repo public with an MIT license.
Please credit me if you use any of the code I've written!

General:
- https://flask.palletsprojects.com/en/stable/
- https://jinja.palletsprojects.com/en/stable/templates/

Styling:
- https://getbootstrap.com/
- https://datatables.net/manual/installation
- https://select2.org/

Data viz stuff:
- https://seaborn.pydata.org/examples/index.html
- https://www.chartjs.org/docs/latest/
- https://d3js.org/d3-scale-chromatic