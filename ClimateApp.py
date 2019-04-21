#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 18:52:01 2019

@author: yevgeniykhmelnitskiy
"""



from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#Database setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#for reference if you wanted to look at the tables joined
conn = engine.connect()

session = Session(engine)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Welcome to the Climate App<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        )
@app.route("/api/v1.0/precipitation")
def precipitation():
    

#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
    dateprcpresults = session.query( Measurement.date, Measurement.prcp).all()
    
    datesAndPrecipitation = []
    for date, prcp in dateprcpresults:
        DatePrecip = {}
        DatePrecip["date"] = date
        DatePrecip["prcp"] = prcp
        datesAndPrecipitation.append(DatePrecip)
        
    return jsonify(datesAndPrecipitation)

@app.route("/api/v1.0/stations")
def station():

#Return a JSON list of stations from the dataset.
    stationresults = session.query(Station.station).all()
    Stations = []
    for station in stationresults:
        stations = {}
        stations["station"] = station
        Stations.append(stations)
        
    return jsonify(Stations)


@app.route("/api/v1.0/tobs")
def date_temp_from_a_year_from_last_data_point():
#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    first_date = dt.date(int(last_date[0][:4]), int(last_date[0][5:7]), int(last_date[0][8:11])) - dt.timedelta(weeks=52)
#first_date = parsed_last_date - dt.timedelta(weeks=52)
    sel1 = [Measurement.date, 
        Measurement.tobs]



    date_tobsresults = session.query(*sel1).\
    filter(Measurement.date >= first_date).\
    order_by(Measurement.date).all()
    DateTobs = []
    for date, tobs in  date_tobsresults:
        datetobs = {}
        datetobs["date"] = date
        datetobs["tobs"] = tobs
        DateTobs.append(datetobs)
    return jsonify(DateTobs)
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>") 
def Min_Max_Avg_per_Start_Date(start):
    
    StartDateresults = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    StartDate = []
    for mini, avg, maxa in StartDateresults:
        startdate = {}
        startdate["min"] = mini
        startdate["avg"] = avg
        startdate["max"] = maxa
        StartDate.append(startdate)
    return jsonify(StartDate)
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>/<end>")
def Min_Max_Avg_per_Start_Date_End_Date(start,end):
    
    StartEndDateresults = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    StartEndDate = []
    for mini, avg, maxa in StartEndDateresults:
        startenddate = {}
        startenddate["min"] = mini
        startenddate["avg"] = avg
        startenddate["max"] = maxa
        StartEndDate.append(startenddate)
    return jsonify(StartEndDate)

if __name__ == "__main__":
    app.run(debug=True)