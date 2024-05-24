from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    vehicle_type = None
    forecast_type = None
    num_steps = None
    image_path = None
    logo_path = None

    logo_paths = {
        "gasolineford": "images/gasolineford/logo.png",
        "gasolinechevrolet": "images/gasolinechevrolet/logo.png",
        "gasolinetoyota": "images/gasolinetoyota/logo.png",
        "electrictesla": "images/electrictesla/logo.png",
        "electricford": "images/electricford/logo.png",
        "electrichyundai": "images/electrichyundai/logo.png",
    }

    if request.method == "POST":
        vehicle_type = request.form.get("vehicle_type")
        forecast_type = request.form.get("forecast_type")
        logo_path = logo_paths.get(vehicle_type, "")

        if forecast_type == "forecast_vs_actual":
            image_path = f"/static/images/{vehicle_type}/arima_forecast_vs_actual.png"
        elif forecast_type == "steps":
            num_steps = request.form.get("num_steps")
            image_path = f"/static/images/{vehicle_type}/forecast_{num_steps}_steps.png"

    return render_template("index.html", 
                           image_path=image_path, 
                           vehicle_type=vehicle_type,
                           forecast_type=forecast_type,
                           logo_path=logo_path,
                           num_steps=num_steps)