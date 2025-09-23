import flask
from flask import Flask, render_template, request
import numpy as np
from utils import predict_with_dt, category_mapping, get_keys_from_value
from pickle import load

app = Flask(__name__)

# Load the models
dt_genus = load(open('../models/decision_tree_genus_model.pkl', "rb"))
dt_common_name = load(open('../models/decision_tree_common_name_model.pkl', "rb"))


# Define routes

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            length = float(request.form['length'])
            weight = float(request.form['weight'])
            age_class = request.form['age_class']
            sex = request.form['sex']
            habitat_type = request.form['habitat_type']
            country_region = request.form['country_region']

            genus, common_name = predict_with_dt(length, weight, age_class, sex, habitat_type, country_region, dt_genus, dt_common_name, category_mapping)

            return render_template('index.html', genus=genus, common_name=common_name)

        except Exception as e:
            return render_template('index.html', error=str(e))
        #correr otro html de error

    return render_template('index.html', genus=None, common_name=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
