# Mario Kart 8 Deluxe Time Trials Visualiser

Personal project combining my hobby with some data visualisation and analysis.
This is mostly a practical way to try learn more data vis and web dev.
Currently, most back-end stuff and a lot of front-end things are done.
Next goal is to keep working on the individual track pages and improve the graphs.

## High-level Goals
See `todo.md` for more specific stuff.
- [x] Back-end stuff like parsing and combining data, simple visualisations
- [x] Set up Flask for a basic web app
- [x] Set up SQLite for database, design schemas
- [x] Design pages for different features using Bootstrap
- [x] Front-end libraries for things like data tables, interactive graphs
- [ ] Testing, better input validation, error handling, etc.

## Overview
The application is built using Flask, which is run with the following command:
```
python -m flask run
```
Once running, the application should be running on [localhost:5000](http://127.0.0.1:5000/).
Append `--debug` to run in debug mode.

It is strongly recommended to be working in a virtual environment. This is made pretty simple by running the following commands:
```
python -m venv env          # to init
.\env\Scripts\activate      # Windows
source env/bin/activate     # MacOS / Linux
deactivate                  # to exit
```

### Requirements
TODO

### Initialising the database
To initialise (or drop and re-create) the database file, run the following command:
```
python -c "import db; db.init_db()"
```
This will create the tables as specified in the `schema.sql` file.

## References / Resources
- https://flask.palletsprojects.com/en/stable/
- https://jinja.palletsprojects.com/en/stable/templates/

### Styling
- https://getbootstrap.com/
- https://datatables.net/manual/installation
- https://select2.org/

### Data viz stuff
- https://seaborn.pydata.org/examples/index.html
- https://www.chartjs.org/docs/latest/
- https://imagecolorpicker.com/color-code/2596be
- https://www.npmjs.com/package/colormap
- https://d3js.org/d3-scale-chromatic