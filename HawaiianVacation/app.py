# Import the dependencies.

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import datetime as dt

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

# session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate App. Please use the following routes:<br/>"
        f"/api/v1.0/precipitation for 12 months of precipitation data<br/>"
        f"/api/v1.0/stations for a list of stations from the dataset<br/>"
        f"/api/v1.0/tobs for 12 months of temperature observations from the most active weather station<br/>"
        f"/api/v1.0/<start> for tmin, tmax, and tavg for all dates greater than or equal to the start date<br/>"
        f"/api/v1.0/<start>/<end> for tmin, tmax, and tavg for all dates from the start date to the end date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    prior_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precip_query = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prior_year).all()
    
    session.close()

    precip_dict = dict(precip_query) # https://stackoverflow.com/questions/58658690/retrieve-query-results-as-dict-in-sqlalchemy, referenced for how to convert query rows to dictionary

    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    prior_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    measurement_station_combined = session.query(Measurement.station, Station.name, func.count(Measurement.station)).\
    filter(Measurement.station == Station.station).group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

    most_active_station = measurement_station_combined[0].station

    twelve_months_temp = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= prior_year).all()
    
    session.close()

    temp_obs = list(np.ravel(twelve_months_temp))

    return jsonify(temp_obs)

@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

    # canonicalized = start.

    data_from_start_date = session.query(Measurement.tobs).\
        filter(Measurement.date >= start).all()    

    session.close()

    temp_data_from_date = list(np.ravel(data_from_start_date))

    return jsonify(temp_data_from_date)


if __name__ == "__main__":
    app.run(debug=True)

# session.close()