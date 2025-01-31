import os
from flask import Flask, request, jsonify, render_template
import pandas as pd
from joblib import load
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from geopy.geocoders import Nominatim

# Initialize Flask app
app = Flask(__name__)

# Load model (ensure the correct path)
MODEL_PATH = 'model/rf_model'
try:
    rfc = load(MODEL_PATH)
    print('Model loaded successfully')
except FileNotFoundError:
    print(f"Model file not found at {MODEL_PATH}")
    rfc = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not rfc:
        return "Model is not loaded, cannot make predictions.", 500

    try:
        address = request.form['Location']
        geolocator = Nominatim(user_agent="geoapi")
        location = geolocator.geocode(address)

        if location is None:
            return render_template('result.html', prediction="Invalid address")

        print(location.address)
        lat = [location.latitude]
        log = [location.longitude]
        latlong = pd.DataFrame({'latitude': lat, 'longitude': log})
        print(latlong)

        # Assuming a timestamp field is provided
        DT = request.form['timestamp']
        latlong['timestamp'] = DT

        # Ensure the data matches the model's expected input format
        my_prediction = rfc.predict(latlong)

        return render_template('result.html', prediction=my_prediction)

    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while processing your request.", 500

if __name__ == '__main__':
    app.run(debug=True)
