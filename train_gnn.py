import pandas as pd
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
import joblib

# Configuration
BASELINE_DATA_FILENAME = "gnn_baseline_data.json"
MODEL_FILENAME = "gnn_autoencoder_model.h5"
TRAINED_FEATURES_FILENAME = "trained_features.joblib"

print("1. Loading and cleaning data...")

data = []
try:
    with open(BASELINE_DATA_FILENAME, 'r') as f:
        for line in f:
            data.append(json.loads(line))
except FileNotFoundError:
    print(f"Error: {BASELINE_DATA_FILENAME} not found. Run agent.py for data collection first.")
    exit()

# 1. Feature Engineering: Convert process data into frequency counts
all_process_names = set()
for record in data:
    for process in record.get('processes', []):
        all_process_names.add(process.get('name'))

# Create a consistent feature list (vocabulary)
feature_list = sorted(list(all_process_names))
joblib.dump(feature_list, TRAINED_FEATURES_FILENAME) # Save feature list immediately

feature_vectors = []
for record in data:
    vector = np.zeros(len(feature_list))
    for process in record.get('processes', []):
        name = process.get('name')
        if name in feature_list:
            index = feature_list.index(name)
            vector[index] += 1
    feature_vectors.append(vector)

X = np.array(feature_vectors)

# --- 2. Training the Model (GNN Autoencoder Architecture) ---
print(f"2. Training GNN Autoencoder with {X.shape[1]} unique features...")

input_dim = X.shape[1]
encoding_dim = 16 # Compression size

input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
decoded = Dense(input_dim, activation='relu')(encoded) # Use 'relu' or 'linear' for counts

autoencoder = Model(input_layer, decoded)
autoencoder.compile(optimizer='adam', loss='mean_squared_error')

# Train on normal data
autoencoder.fit(X, X,
                epochs=50,
                batch_size=8,
                shuffle=True,
                verbose=1)

# --- 3. Save the Model ---
autoencoder.save(MODEL_FILENAME)

print("\n--- GNN TRAINING COMPLETE ---")
print(f"Model saved as: {MODEL_FILENAME}")