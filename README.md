# Mario Kart 8 Deluxe Time Trials Visualiser

Personal project combining my hobby with some data visualisation and analysis. 
Ideally becomes a web app with all the features I want to implement. 
Back-end basics are mostly done so now want to make a web-app for a decent UI to interact with.

## High-level Goals
- [x] Back-end stuff like parsing and combining data, simple visualisations
- [x] Set-up Flask for a basic web app
- [ ] Design pages for different features using Bootstrap (?)
- [x] SQLite for database, design schemas
- [ ] Front-end libraries for things like data tables, interactive graphs, templates

### Future considerations:
- [ ] Support for track name abbreviations (e.g., MKS == Mario Kart Stadium)
- [ ] Practice suggestions based on select criteria (such as choosing from worst 10 times)
- [ ] Get WR video and other info when looking at specific track pages
- [ ] Interactive visualisations (like tooltips on hover)
- [ ] Support for different categories like 200 and NITA

## Overview
The application is built using Flask, which is run with the following command:
```
python -m flask run
```
Once running, the application is hosted locally on [localhost:5000](http://127.0.0.1:5000/).
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

### Initialising the Database
To initialise (or drop and re-create) the database file, run the following command:
```
python -c "import db; db.init_db()"
```
This will create the tables as specified in the `schema.sql` file.

## References / Resources
- https://flask.palletsprojects.com/en/stable/
- https://jinja.palletsprojects.com/en/stable/templates/
- https://getbootstrap.com/
- https://seaborn.pydata.org/examples/index.html