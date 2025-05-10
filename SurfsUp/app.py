# # Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


#################################################
# Database Setup
#################################################

# Create the connection to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
base = automap_base()

# Reflect the tables
base.prepare(autoload_with=engine)

# Save reference to the table
measurement = base.classes.measurement
station = base.classes.station

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
        f"Welcome to the Hawaii Climate API!<br><br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/&lt;start&gt;<br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br>"
    )
    
# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Retrieve the most recent date in the dataset
    most_recent_date = session.query(func.max(measurement.date)).first()
   
    # Calculate the date one year from the last date in data set.
    one_year_ago  = (pd.to_datetime(most_recent_date[0]) - pd.DateOffset(years=1)).date()

    # Query the  precipation data one year ago
    results = session.query(measurement.date, measurement.prcp)\
    .filter(measurement.date >= one_year_ago).all()

    # Convert the query results into a dictionary
    precipitation = {date: prcp for date, prcp in results}

    return jsonify(precipitation)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
   
    # Query the station IDs and their counts
    results = session.query(
        measurement.station, 
        func.count(measurement.station).label("station_count")
    ).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

    # Convert query results to a dictionary
    station_list = [
        {"station": station, "count": count} 
        for station, count in results
    ]
    return jsonify(station_list)

#  TOBS Route (Temperature Observations) for the most active station 
@app.route("/api/v1.0/tobs")
def tobs():
    
    # Identify the  most active weather station
    most_active_station = session.query(
        measurement.station, 
        func.count(measurement.station).label("station_count")
        ).group_by(measurement.station
    ).order_by(func.count(measurement.station).desc()).first()

    most_active_station_id = most_active_station[0]  # Extract the station ID

    # Retrieve the most recent date in the dataset
    most_recent_date = session.query(func.max(measurement.date)).first()

    # Query the tobs data of the most-active station one year ago
    one_year_ago  = (pd.to_datetime(most_recent_date[0]) - pd.DateOffset(years=1)).date()
    results = session.query(measurement.date, measurement.tobs).filter(
        measurement.station == most_active_station_id,
        measurement.date >= one_year_ago).all()
    
    # Convert the query  results to a dictionary
    tobs = [{"date": date, "tobs": temp} for date, temp in results]

    return jsonify(tobs)
    
# Start Date Route
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Verify if the provided start date exists in the dataset
    dates = [row[0] for row in session.query(measurement.date).distinct().all()]
    if start not in dates:
        return jsonify({"error": f"Start date {start} not found in dataset."})
    
    # Query temperature statistics from the start date onward
    results = session.query(
        func.min(measurement.tobs).label('TMIN'),
        func.max(measurement.tobs).label('TMAX'),
        func.avg(measurement.tobs).label('TAVG')
    ).filter(measurement.date >= start).all()

    # Convert the query results to a dictionary
    temperature = {
        "Start Date": start,
        "TMIN": results[0].TMIN,   
        "TMAX": results[0].TMAX,
        "TAVG": round(results[0].TAVG, 1) 
        }

    return jsonify(temperature)

# Start and End Date Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    # Verify  if the provided start and end dates exist in the dataset
    dates = [row[0] for row in session.query(measurement.date).distinct().all()]
    if start not in dates:
        return jsonify({"error": f"Start date {start} not found in dataset."})
    if end not in dates:
        return jsonify({"error": f"End date {end} not found in dataset."})

    # Query temperature statistics from the given start and end date
    results = session.query(
        func.min(measurement.tobs).label('TMIN'),
        func.max(measurement.tobs).label('TMAX'),
        func.avg(measurement.tobs).label('TAVG')
    ).filter(measurement.date >= start).filter(measurement.date <= end).all()

    # Convert the results to a dictionary
    temperature = {
        "Start Date": start,
        "End Date": end,
        "TMIN": results[0].TMIN,
        "TMAX": results[0].TMAX,
        "TAVG": round(results[0].TAVG, 1)   
        }
      
    return jsonify(temperature)

# Close the session
session.close()


if __name__ == '__main__':
    app.run(debug=True)

