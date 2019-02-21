# 1. Import Flask
from flask import Flask


# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def xxx():
   

@app.route("/api/v1.0/stations")
def station_list():

@app.route("/api/v1.0/tobs")
def tob_year_ago():

@app.route("/api/v1.0/<start>")
def temperature_stats_by_start_date(start):
  
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_by_date_range(start,end):
  
  

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)