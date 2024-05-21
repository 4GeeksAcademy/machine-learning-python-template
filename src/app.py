from flask import Flask, render_template, request
import os
from pickle import load
import joblib
from math import sqrt
from sklearn.metrics import mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
models_dir = os.path.join(os.path.dirname(__file__), '../models/')

# Load models
models = {
    'Electric Ford Model': joblib.load(os.path.join(models_dir, 'eford_model.sav')),
    'Electric Hyundai Model': joblib.load(os.path.join(models_dir, 'ehyundai_model.sav')),
    'Electric Tesla Model': joblib.load(os.path.join(models_dir, 'tesla_model.sav')),
    'Gasoline Chevrolet Model': joblib.load(os.path.join(models_dir, 'gchev_model.sav')),
    'Gasoline Ford Model': joblib.load(os.path.join(models_dir, 'gford_model.sav')),
    'Gasoline Toyota Model': joblib.load(os.path.join(models_dir, 'gtoy_model.sav'))
}

@app.route('/')
def index():
    return render_template('index.html', models=models.keys())

@app.route('/result', methods=['POST'])
def result():
    selected_model = request.form['model']

    # Retrieve the selected model object
    selected_model_object = models[selected_model]

    # Load necessary data based on the selected model
    data_dir = os.path.join(os.path.dirname(__file__), 'data/processed/')
    if selected_model == 'Electric Ford Model':
        data_file_path = os.path.join(data_dir, 'sorted_electric_ford.csv')
    elif selected_model == 'Electric Hyundai Model':
        data_file_path = os.path.join(data_dir, 'sorted_electric_hyundai.csv')
    elif selected_model == 'Electric Tesla Model':
        data_file_path = os.path.join(data_dir, 'sorted_electric_tesla.csv')
    elif selected_model == 'Gasoline Chevrolet Model':
        data_file_path = os.path.join(data_dir, 'sorted_gasoline_chevrolet.csv')
    elif selected_model == 'Gasoline Ford Model':
        data_file_path = os.path.join(data_dir, 'sorted_gasoline_ford.csv')
    elif selected_model == 'Gasoline Toyota Model':
        data_file_path = os.path.join(data_dir, 'sorted_gasoline_toyota.csv')
    else:
        # Handle the case when the selected model is not recognized
        return render_template('index.html', models=models.keys(), error_message='Selected model not recognized')

    # Load data for the selected model
    data = pd.read_csv(data_file_path)

    # Generate visualization for the selected model
    if selected_model == 'Gasoline Toyota Model':
        plot_url = generate_visualization(selected_model_object, data)
    else:
        plot_url = generate_dummy_visualization(selected_model)

    return render_template('index.html', models=models.keys(), error_message='Selected model not recognized')

def generate_visualization(model, data_file_path):
    df = pd.read_csv(data_file_path)

    train_size = int(len(df) * 0.8)
    train, test = df[:train_size], df[train_size:]

    train_diff = train.diff().dropna()
    train_diff

    # test_stationarity(train_diff)

    forecast_steps = len(test)
    forecast, conf_int = model.predict(n_periods=forecast_steps, return_conf_int=True)

    # Calculate RMSE
    rmse = sqrt(mean_squared_error(test, forecast))
    print('Test RMSE: %.3f' % rmse)

    last_element_index = train.index[-1]
    last_element_value = train.iloc[-1]

    last_element_series_forecast = pd.Series([last_element_value], index=[last_element_index])
    forecast_series = pd.concat([last_element_series_forecast, pd.Series(forecast, index=test.index)])
    test_series = pd.concat([train, test])

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(train.index, train, color='steelblue', label='Train')
    ax.plot(test_series.index, test_series, color='orange', label='Test')
    ax.plot(forecast_series.index, forecast_series, color='red', linestyle='--', label='Forecast')
    ax.fill_between(test.index, conf_int[:, 0], conf_int[:, 1], color='pink', alpha=0.3, label='Confidence Interval')
    ax.set_title(f'{selected_model} ARIMA Forecast vs Actual')
    ax.set_xlabel('Year')
    ax.set_ylabel('Avg City MPG')
    ax.legend()

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)  # Close the figure to free up memory
    plt.close('all')

    return f'data:image/png;base64,{plot_url}'

def generate_dummy_visualization(model_name):
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3], [0, 1, 4, 9], label=model_name)
    ax.set_title(f'Visualization for {model_name}')
    ax.legend()

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)  # Close the figure to free up memory

    return f'data:image/png;base64,{plot_url}'

if __name__ == '__main__':
    app.run(debug=True)