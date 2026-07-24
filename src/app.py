from flask import Flask, request, render_template
import os   
import joblib
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "models", "salary_predictor_model.sav")

model = joblib.load(model_path)
#model = load(open("/workspaces/Appwebs/models/salary_predictor_model.sav", "rb"))


@app.route("/", methods = ["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        
        val1 = float(request.form["val1"])
        val2 = float(request.form["val2"])
        val3 = float(request.form["val3"])
        
        data = [[val1, val2, val3]]
        salary = model.predict(data)[0]
        rounded_salary = round(salary, -3)
        prediction = f"${rounded_salary:,.0f} dólares"
    
    return render_template("index.html", prediction=prediction)