from flask import Flask, request, render_template 
import os
from joblib import load

app = Flask(__name__)

model =load(open("../models/salary_predictor_model.sav","rb")) 
print("modelo cargado")


# Generar opciones dinámicas desde dataset
#options = {
  #  "job_title": sorted(df["job_title"].dropna().unique()),
   # "education_level": sorted(df["education_level"].dropna().unique()),
    #"industry": sorted(df["industry"].dropna().unique()),
    #"company_size": sorted(df["company_size"].dropna().unique()),
    #"location": sorted(df["location"].dropna().unique())
#}

def preprocess_input(data):
    df_input = pd.DataFrame([data])

    if columns is not None:
        df_input = pd.get_dummies(df_input)

        for col in columns:
            if col not in df_input:
                df_input[col] = 0

        df_input = df_input[columns]

    return df_input


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        try:
            input_data = {
                "job_title": request.form.get("job_title"),
                "experience_years": int(request.form.get("experience_years")),
                "education_level": request.form.get("education_level"),
                "skills_count": int(request.form.get("skills_count")),
                "industry": request.form.get("industry"),
                "company_size": request.form.get("company_size"),
                "location": request.form.get("location"),
                "remote_work": int(request.form.get("remote_work")),
                "certifications": int(request.form.get("certifications"))
            }

            processed = preprocess_input(input_data)
            prediction = round(model.predict(processed)[0], 2)

        except Exception as e:
            prediction = f"Error: {e}"

    return render_template("index.html", prediction=prediction, options=options)

if __name__ == "__main__":
    app.run(debug=True)