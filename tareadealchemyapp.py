# Importing dependencies
##############################################
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
from datetime import date, time, datetime

# Setup
##############################################

###### Database Setup 
engine=create_engine("sqlite:///hawaii.sqlite")

###### Reflecting Databases 
Base= automap_base()

###### Reflecting tables 
Base.prepare(engine, reflect=True)

###### Reflecting tables 
Measurement= Base.classes.measurement
Station= Base.classes.station

###### Flask setup 
app= Flask(__name__)

# Definig Available Routes
##############################################

## Home route:
##############################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Weather Site!<br/>"
        f"These are the available routes:<br/>"
        f"/api/v1.0/precipitation/<br/>"
        f"/api/v1.0/stations/<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start>"
        f"/api/v1.0/temp/<start>/<end>"
    )

## Precipitation route:
##############################################
@app.route('/api/v1.0/precipitation/')
def precipitation():

    ## Opening session
    session=Session(engine)

    # Setup
    most_recent_date=(dt.date(year=2017, month=8, day=23))
    query_l12m=most_recent_date-dt.timedelta(days=365)

    # Querying
    results_query_l12m = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>=query_l12m).all()

    # Passing results into a dictionary, date as the key
    precipitation = {date: prcp for date, prcp in results_query_l12m}  

    # Returning a json format  
    return jsonify(precipitation)

    ## Closing session
    session.close()

## Stations route:
##############################################
@app.route('/api/v1.0/stations')
def stations():

    ## Opening session
    session=Session(engine)

    # Querying
    all_stations=session.query(Station.station).all()

    # Passing results into a dictionary, station as the key
    stations=list(np.ravel(all_stations))

    # Returning a json format  
    return jsonify(stations)

    ## Closing session
    session.close()

## Best Station route ('USC00519281'):
##############################################
@app.route('/api/v1.0/tobs')
def top_station():

    ## Opening session
    session=Session(engine)

    # Setup
    most_recent_date=(dt.date(year=2017, month=8, day=23))

    # Querying observations for the last year of data
    query_l12m=most_recent_date-dt.timedelta(days=365)

    results=session.query(Measurement.tobs).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date>=query_l12m).all()
    
    # Passing results into a dictionary
    top_station=list(np.ravel(results))

    # Returning a json format  
    return jsonify(top_station)

    ## Closing session
    session.close()

## Start route:
##############################################

@app.route("/api/v1.0/temp/<start>")

## Start- End route:
##############################################

@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):   

    ## Opening session
    session=Session(engine)

    sel=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end : 
        results=session.query(*sel).filter(Measurement.date >= start).all()
        all_temps=list(np.ravel(results))
        return jsonify(all_temps)

    results=session.query(*sel).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    
    # Passing results into a dictionary
    all_temps=list(np.ravel(results))

     # Returning a json format  
    return jsonify(all_temps)

    ## Closing session
    session.close()
  
## Running script
if __name__ == '__main__':    
    app.run()