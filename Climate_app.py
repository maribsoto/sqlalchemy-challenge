# Dependencies
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from Climate_Analysis_MBS import results_dic, my_stations_dic, my_tobs, stats_dict, end_stats_dict

from flask import Flask, jsonify
import os

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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Home Page and list of all the available api routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_dates<br/>"
        f"/api/v1.0/start_end_dates/<end>"
    )
# IMPORTANT: Reading ALL the below dictionaries from Climate_Analysis_MBS.py and
# returning as a json representation

###################################################
# /api/v1.0/precipitation 
# - Convert the query results to a dictionary using date as the 
# key and prcp as the value
# - Return the JSON representation of your dictionary
###################################################


@app.route("/api/v1.0/precipitation")
def index():
    """Jasonified precipitation query results"""
    return results_dic



###################################################
# /api/v1.0/stations
# - Return a JSON list of stations from the dataset
###################################################

# Reading variable my_stations_dic from Climate_Analysis_MBS.py and 
# retutrning a json list of stations names and IDs

@app.route("/api/v1.0/stations")
def statn():
    """Jasonified stations list"""
    return my_stations_dic

###################################################
# /api/v1.0/tobs
# - Query the dates and temperature observations of the most 
# active station for the last year of data.
# - Return a JSON list of temperature observations (TOBS) 
# for the previous year.
###################################################

#
@app.route("/api/v1.0/tobs")
def tob():
    """Jasonified TOBS list"""
    return my_tobs


###################################################
# /api/v1.0/<start>
# - Return a JSON list of the minimum temperature, the average temperature,
# and the max temperature for a given start or start-end range.
# - When given the start only, calculate TMIN, TAVG, and TMAX for all dates 
# greater than and equal to the start date.
###################################################

@app.route("/api/v1.0/start_dates")
def strt():
    """Jasonified MIN, AVG, MAX TOBS From Aug 1, 2017"""
    return stats_dict

###################################################
# /api/v1.0/<start>/<end>
# - Return a JSON list of the minimum temperature, the average temperature,
# and the max temperature for a given start or start-end range.
# - When given the start only, calculate TMIN, TAVG, and TMAX for all dates 
# greater than and equal to the start date.
###################################################

@app.route("/api/v1.0/start_end_dates/<end>")
def start_end():
    """Jasonified MIN, AVG, MAX TOBS between Aug 1-20, 2017"""
    return end_stats_dict  

if __name__ == '__main__':
    app.run(debug=True)