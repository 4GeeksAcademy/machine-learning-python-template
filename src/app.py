from flask import Flask, request, render_template
from pickle import load

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    image_path = None
    vehicle_type = None
    forecast_type = None
    num_steps = None

    if request.method == "POST":
        vehicle_type = request.form.get("vehicle_type")
        forecast_type = request.form.get("forecast_type")

        if forecast_type == "forecast_vs_actual":
            # By default, Flask renders static files from the static directory
            image_path = f"/static/images/{vehicle_type}/arima_forecast_vs_actual.png"
        elif forecast_type == "steps":
            num_steps = request.form.get("num_steps")
            image_path = f"/static/images/{vehicle_type}/forecast_{num_steps}_steps.png"

    return render_template("index.html", 
                           image_path=image_path, 
                           vehicle_type=vehicle_type,
                           forecast_type=forecast_type,
                           num_steps=num_steps)

    