# Import the dependencies.

import warnings
warnings.filterwarnings("ignore")

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# engine = create_engine("sqlite:///Resources//hawaii.sqlite")

# https://stackoverflow.com/questions/4636970/sqlite3-operationalerror-unable-to-open-database-file, referenced for how to fix unable to open database file error
engine = create_engine("sqlite:///C:\\Users\\dmrop\\Desktop\\Assignments\\Starter_Code\\sqlalchemy-challenge\\HawaiianVacation\\Resources\\hawaii.sqlite")



# reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(autoload_with=engine)

# Save references to each table

Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

