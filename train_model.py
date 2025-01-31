import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Create directory for saving the model if it doesn't exist
if not os.path.exists('model'):
    os.makedirs('model')

# Generate some mock data for training
np.random.seed(42)

# Mock dataset with features: latitude, longitude, year, month, day, hour, weekday, etc.
data = {
    'latitude': np.random.uniform(19.0, 25.0, 1000),  # Random latitudes in India
    'longitude': np.random.uniform(72.0, 85.0, 1000),  # Random longitudes in India
    'year': np.random.randint(2010, 2025, 1000),  # Random year between 2010 and 2025
    'month': np.random.randint(1, 13, 1000),  # Random month between 1 and 12
    'day': np.random.randint(1, 32, 1000),  # Random day between 1 and 31
    'hour': np.random.randint(0, 24, 1000),  # Random hour between 0 and 23
    'weekday': np.random.randint(0, 7, 1000),  # Random weekday (0=Monday, 6=Sunday)
    'crime_type': np.random.randint(0, 6, 1000)  # Random crime type (0-5)
}

# Create a DataFrame
df = pd.DataFrame(data)

# Features (X) and Target (y)
X = df.drop('crime_type', axis=1)
y = df['crime_type']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rfc.fit(X_train, y_train)

# Save the model
model_path = 'model/rf_model'
joblib.dump(rfc, model_path)

print(f"Model trained and saved at {model_path}")
