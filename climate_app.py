import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station

last_data_point = dt.date(2017, 8, 23)
year_from_last = last_data_point - dt.timedelta(days=365)

Measurement = Base.classes.measurement
Station = Base.classes.station
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)
app = Flask(__name__)

@app.route("/")
def index():
    return (
        f"Routes:<br />"
        f"<br />"
        f"/api/v1.0/precipitation<br />"
        f"/api/v1.0/stations<br />"
        f"/api/v1.0/tobs<br />"
        f"/api/v1.0/temp/start/end<br />"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_from_last).all()
    precip = {}
    for result in prcp_query:
        prcp_list = {result.date: result.prcp, "prcp": result.prcp}
        precip.update(prcp_list)

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def station():
    stations_list = session.query(Station.station).all()
    stationz = list(np.ravel(stations_list))
    return jsonify(stationz)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_from_last).all()
    tobs_list = list(np.ravel(tobs_query))
    return jsonify(tobs_list)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def calc_temps(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.

    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """

    if end != "":
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
            func.max(Measurement.tobs)).filter(Measurement.date.between(year_from_last, last_data_point)).all()
        t_stats = list(np.ravel(temp_stats))
        return jsonify(temp_stats)

    else:
        temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
            func.max(Measurement.tobs)).filter(Measurement.date > last_data_point).all()
        t_stats = list(np.ravel(temp_stats))
        return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(port=9000, debug=True)