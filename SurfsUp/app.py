# # Import the dependencies.
# import datetime as datetime
import numpy as np
import pandas as pd
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


#################################################
# Database Setup
#################################################

# Create the connection to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# create a base class for the ORM
Base = automap_base()
# base.prepare(engine, reflect=True)
Base.prepare(autoload_with=engine)


# save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement

# create a session 
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
        f"/api/v1.0/&lt;startdate&gt; (Date format: YYYY-MM-DD)<br>"
        f"/api/v1.0/&lt;startdate&gt;/&lt;enddate&gt; (Date format: YYYY-MM-DD for both start and end dates)<br>"
    )

    
# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Get the most recent date
    most_recent_date = session.query(func.max(measurement.date)).scalar()

    # Calculate the date one year from the last date in data set.
    last_12_months = (pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)).date()

    # Query the date and precipitation scores in the last 12 months
    precipitation = session.query(measurement.date, measurement.prcp)\
    .filter(measurement.date >= last_12_months).all()

    # Convert the result to dictionary
    precipitation_dict = {date: prcp for date, prcp in precipitation}

    return jsonify(precipitation_dict)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
   
    # Query station data from the station table
    station = session.query(station.station).all()
    
    # Create a dictionary from the row data and append to a list of station data
    station_data = []
    for row in results:
        station_dict = {
            "id": row.id,
            "station": row.station,
            "name": row.name,
            "latitude": row.latitude,
            "longitude": row.longitude,
            "elevation": row.elevation
        }
        station_data.append(station_dict)
       
    return jsonify(stations_list)

#  TOBS Route (Temperature Observations) for the most active station 
@app.route("/api/v1.0/tobs")
def tobs():
    
    most_active_station = "USC00519281"

    # Get the most recent date
    most_recent_date = session.query(func.max(measurement.date)).scalar()

    # Calculate the date one year from the last date in data set.
    last_12_months = (pd.to_datetime(most_recent_date) - pd.DateOffset(years=1)).date()
    
    # Query the temperature observation data(tobs) in the last 12 months
    tobs = session.query(measurement.date, measurement.tobs).filter(
        measurement.station == most_active_station,
        measurement.date >= last_12_months).all()
    
    # Convert the tobs results to dictionary
    tobs_list = [{"date": date, "tobs": temp} for date, temp in tobs]

    return jsonify(tobs_list)

# Start Date Route
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Check if start and end dates exist in the dataset
    dates = [row[0] for row in session.query(measurement.date).distinct().all()]
    if start not in dates:
        return jsonify({"error": f"Start date {start} not found in dataset."})
    
    # Query temperature statistics from the given start date onward
    results = session.query(
        func.min(measurement.tobs).label('TMIN'),
        func.max(measurement.tobs).label('TMAX'),
        func.avg(measurement.tobs).label('TAVG')
    ).filter(measurement.date >= start).all()

    # Convert the results to a dictionary
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

 # Check if start and end dates exist in the dataset
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

