import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"Welcome to the API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/precipitation/2010-01-24/0.01<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2012-02-28<br/>"
        f"/api/v1.0/2012-02-28/2012-03-05<br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = (session
        .query(Measurement.date,Measurement.prcp)
        .filter(Measurement.prcp>=0)
        .order_by(Measurement.date).all())
        
    all_prcps = []
    for prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = prcp.date
        prcp_dict["prcp"] = prcp.prcp
        all_prcps.append(prcp_dict)

    return jsonify(all_prcps)

    

@app.route("/api/v1.0/precipitation/<key>/<value>")
def precipitation_arbitrary_key(key, value):
    #Convert the query results to a Dictionary 
    #using date as the key and prcp as the value.

    results = (session
        .query(Measurement.id,Measurement.date,Measurement.prcp,Measurement.tobs,Measurement.station)
        .filter(Measurement.date==key)
        .filter(Measurement.prcp==value)
        .all())

    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["id"] = measurement.id
        measurement_dict["date"] = measurement.date
        measurement_dict["prcp"] = measurement.prcp
        measurement_dict["tobs"] = measurement.tobs
        measurement_dict["station"] = measurement.station
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)


@app.route("/api/v1.0/stations")
def station_list():
    #Return a JSON list of stations from the dataset.

    results = (session
        .query(Station.id,Station.station, Station.name, Station.latitude, Station.longitude)
        .all())

    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tob_year_ago():

    #find a date, a year from the last data point.
    query_latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()# latest Date
    dt_latest_date = dt.datetime.strptime(query_latest_date[0], '%Y-%m-%d')# latest Date in datetime format
    year_ago_date = dt_latest_date - dt.timedelta(days=365)

    #query for the dates and temperature observations from a year from the last data point.
    results = (session
        .query(Measurement.date, Measurement.tobs)
        .filter(Measurement.date > year_ago_date)
        .order_by(Measurement.tobs).all())

    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    all_tobs_year_ago = []
    for tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = tobs.date
        tobs_dict["tobs"] = tobs.tobs
        all_tobs_year_ago.append(tobs_dict)

    return jsonify(all_tobs_year_ago)


@app.route("/api/v1.0/<start>")
def temperature_stats_by_start_date(start):
#When given the start only, calculate TMIN, TAVG, and TMAX 
# for all dates greater than and equal to the start date.
    results  = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    all_tobs_summary = []
    for tobs in results:
        tobs_dict = {}
        tobs_dict["tmin"] = tobs[0]
        tobs_dict["tavg"] = tobs[1]
        tobs_dict["tmax"] = tobs[2]
        all_tobs_summary.append(tobs_dict)

    return jsonify(all_tobs_summary)

  
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_by_date_range(start,end):
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX 
# for dates between the start and end date inclusive.
     
    results  = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    all_tobs_summary = []
    for tobs in results:
        tobs_dict = {}
        tobs_dict["tmin"] = tobs[0]
        tobs_dict["tavg"] = tobs[1]
        tobs_dict["tmax"] = tobs[2]
        all_tobs_summary.append(tobs_dict)

    return jsonify(all_tobs_summary)
  
  

# flask set up: Define main behavior
if __name__ == "__main__":
    app.run(debug=True)