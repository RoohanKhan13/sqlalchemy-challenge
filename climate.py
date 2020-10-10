import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Design a query to retrieve the last 12 months of precipitation data and plot the results

    # Calculate the date 1 year ago from the last data point in the database

  
    last_year = dt.date(2017,8,23) - dt.timedelta(days= 365)

    year_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year, Measurement.prcp != None).\
    order_by(Measurement.date).all()

    

    return jsonify(dict(year_data))

@app.route("/api/v1.0/stations")
def stations():
    
    active_stations = session.query(Measurement.station,func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    
   

    return jsonify(dict(active_stations))


@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2017,8,23) - dt.timedelta(days= 365)
    highest_tobs = session.query(Measurement.date, Measurement.tobs).\
      filter(Measurement.date >= last_year, Measurement.station == 'USC00519281').\
      order_by(Measurement.tobs).all()

    return jsonify (dict(highest_tobs))

@app.route("/api/v1.0/<start>/<end>")

def calc_temps(start,end):
   
    findings = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    found =[] 
    for row in findings:
        found.append(row.tobs) 
    return (jsonify ({"tempmin": min(found),"tempmax": max(found),"tempavg":np.mean}))
           
            

if __name__ == "__main__":
   app.run(debug=True)


