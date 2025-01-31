# Mario Kart 8 Deluxe Time Trials Visualiser

Personal project combining my hobby with some data visualisation and analysis. 
Ideally becomes a web app with all the features I want to implement. 
Back-end basics are mostly done so now want to make a web-app for a decent UI to interact with.

## Goals
- [x] Back-end stuff like parsing and combining data, simple visualisations
- [ ] Support for name abbrevs
- [x] Set-up Flask for a basic web app
- [ ] Design pages for different features
- [ ] SQLite for database, design schemas, libraries for interaction with web app
- [ ] Front-end libraries for things like data tables, interactive graphs, templates, navigating pages, etc.
- [ ] Update tracking + visualisations

Future considerations:
- Practice suggestions based on select criteria (such as choosing from worst 10 times)
- Kart build stats visualiser (maybe)
- Support for different categories like 200 and NITA

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

## References / Resources
- https://flask.palletsprojects.com/en/stable/
- https://jinja.palletsprojects.com/en/stable/templates/
- https://seaborn.pydata.org/examples/index.html