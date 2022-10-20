#Import from climate_starter
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#Import Flask
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#Part 2: Design Your Climate App Start

#Create an app, being sure to pass __name__
app = Flask(__name__)

#Route = "/"
#Start at the homepage
#List all the available routes
@app.route("/")
def homepage():
    print("Server received request for 'Homepage'")
    return('''
    Welcome to the Module 10 Homepage. <br>
    <br>
    Below are available routes from this page:<br>
    /api/v1.0/precipitation <br>
    /api/v1.0/stations <br>
    /api/v1.0/tobs <br>
    Please replace 'start' and 'end' with a specific date between 2010-01-01 and 2017-08-23 <br>
    /api/v1.0/start <br>
    /api/v1.0/start/end <br>
    ''')

#Route = "/api/v1.0/precipitation"
#Convert the query results to a dictionary by using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    print("Server received request for 'Precipitation' page")
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp = session.query(measurement.date, measurement.prcp)
    prcp_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= query_date).all()
    #Create dictionary
    prcp_dict = dict(prcp_data)
    return jsonify(prcp_dict)
    session.close()

#Route = "/api/v1.0/stations"
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    print("Server received request for 'Stations' page")
    stations_name = session.query(station.station, station.name).all()
    stations_list = list(np.ravel(stations_name))
    return jsonify(stations_list)
    session.close()


#Route = "/api/v1.0/tobs"
#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    print("Server received request for 'Tobs' page")
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_data = session.query(measurement.date, measurement.tobs).filter(measurement.date >= query_date).order_by(measurement.date).all()
    tobs_list = list(np.ravel(tobs_data))
    return jsonify(tobs_list)
    session.close()

#Route = "/api/v1.0/<start> and /api/v1.0/<start>/<end>"
#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    print("Server received request for 'Tobs' page")
    start_date = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
        .filter(measurement.date >= start)\
        .group_by(measurement.date).all()
    start_list = list(np.ravel(start_date))
    return jsonify(start_list)
    session.close()

#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    print("Server received request for 'Tobs' page")
    start_end = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
        .filter(measurement.date >= start)\
        .filter(measurement.date <= end)\
        .group_by(measurement.date).all()
    start_end_list = list(np.ravel(start_end))
    return jsonify(start_end_list)
    session.close()

if __name__ == "__main__":
    app.run(debug=True)