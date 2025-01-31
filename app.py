import os
from flask import Flask, request, render_template, redirect, url_for, session
import pandas as pd
from geopy.geocoders import Nominatim
import random  # Import random module

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

@app.route('/')
def root():
    if not session.get('logged_in'):  # Check if user is logged in
        return redirect(url_for('login'))
    return render_template('index.html', message='Login successful')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Dummy authentication for demonstration
        if username == "admin" and password == "password":
            session['logged_in'] = True  # Mark session as logged in
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove logged-in status from session
    return redirect(url_for('login'))

@app.route('/result.html', methods=['POST'])
def predict():
    if not session.get('logged_in'):  # Restrict access if not logged in
        return redirect(url_for('login'))

    if request.method == 'POST':
        address = request.form['Location']
        geolocator = Nominatim(user_agent="crime_prediction_app")
        location = geolocator.geocode(address, timeout=None)

        if not location:  # Check if geolocation is valid
            return render_template('result.html', prediction="Invalid location provided. Please enter a valid address.", message='Login successful')

        # Validate timestamp format
        DT = request.form['timestamp']
        try:
            pd.to_datetime(DT, errors='raise')
        except ValueError:
            return render_template('result.html', prediction="Invalid timestamp format. Please use 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' format.", message='Login successful')

        # Define a list of random crime predictions
        random_crime_predictions = [
            "No crime expected at this time and location.",
            "Predicted crime: Act 379 - Robbery (Theft of property or valuable items)",
            "Predicted crime: Act 13 - Gambling (Engaging in unlawful gambling activities)", 
            "Predicted crime: Act 279 - Accident (Accidental injury or harm caused to others)",
            "Predicted crime: Act 302 - Murder (The unlawful killing of a person)",
            "Predicted crime: Act 363 - Kidnapping (The unlawful abduction of a person)",
            "Predicted crime: Act 420 - Fraud (Deception for financial gain)"
        ]

        # Select a random prediction
        random_prediction = random.choice(random_crime_predictions)

        # Return the randomly selected prediction
        return render_template('result.html', prediction=random_prediction, message='Login successful')

@app.route('/index.html')
def index():
    if not session.get('logged_in'):  # Restrict access if not logged in
        return redirect(url_for('login'))
    return render_template('index.html', message='Login successful')

@app.route('/home.html')
def home():
    if not session.get('logged_in'):  # Restrict access if not logged in
        return redirect(url_for('login'))
    return render_template('home.html', message='Login successful')

@app.route('/contact.html')
def contact():
    if not session.get('logged_in'):  # Restrict access if not logged in
        return redirect(url_for('login'))
    return render_template('contact.html', message='Login successful')

@app.route('/work.html')
def work():
    if not session.get('logged_in'):  # Restrict access if not logged in
        return redirect(url_for('login'))
    return render_template('work.html', message='Login successful')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
