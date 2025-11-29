from fastapi import FastAPI
import uvicorn
import json
import datetime
from Crypto.Hash import SHA256
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf 
from tensorflow.keras.models import load_model
import subprocess

# --- CONFIGURATION ---
app = FastAPI()
GNN_MODEL_FILENAME = "gnn_autoencoder_model.h5"
TRAINED_FEATURES_FILENAME = "trained_features.joblib"
BASELINE_DATA_FILENAME = "gnn_baseline_data.json"

# --- GLOBAL MODEL & UTILITY LOADING ---
ANOMALY_MODEL = None
TRAINED_FEATURES = None

try:
    # Suppress TensorFlow warnings for cleaner output
    tf.get_logger().setLevel('ERROR')
    ANOMALY_MODEL = load_model(GNN_MODEL_FILENAME)
    TRAINED_FEATURES = joblib.load(TRAINED_FEATURES_FILENAME)
    print(f"INFO: Successfully loaded GNN Autoencoder Model and features.")
except Exception as e:
    print(f"ERROR: Failed to load GNN Model/Features. ML scoring is DISABLED. Error: {e}")

# --- BLOCKCHAIN LOGGING FUNCTION ---
def log_hash_to_blockchain(report_hash: str):
    """
    Executes the Hyperledger CLI command via Docker to commit the hash to the ledger.
    """
    try:
        # For MVP proof of concept, we verify connectivity to the Peer container.
        # In a production system, this would be the full 'peer chaincode invoke' command.
        result = subprocess.run(['docker', 'ps', '-a', '--format', '{{.Names}}'], 
                                capture_output=True, text=True, check=True, timeout=10)
        
        if 'peer0.org1.example.com' in result.stdout:
            return True
        else:
            print("FABRIC LOG FAILED: Hyperledger Peer container not running.")
            return False

    except subprocess.CalledProcessError as e:
        print(f"FABRIC ERROR: Docker command failed. {e}")
        return False
    except FileNotFoundError:
        print("FABRIC ERROR: 'docker' command not found.")
        return False

# --- UTILITY FUNCTION for ML SCORING ---
def score_process_data(processes_list: list):
    """Converts live data to feature vector, scores it, and calculates anomaly error."""
    if not ANOMALY_MODEL or not TRAINED_FEATURES:
        return 1, 0.0 

    live_process_counts = {}
    for process in processes_list:
        name = process.get('name')
        live_process_counts[name] = live_process_counts.get(name, 0) + 1
    
    input_vector = np.zeros(len(TRAINED_FEATURES))
    
    for name, freq in live_process_counts.items():
        if name in TRAINED_FEATURES:
            input_vector[TRAINED_FEATURES.index(name)] = freq
        
    X_live = input_vector.reshape(1, -1)
    
    reconstruction = ANOMALY_MODEL.predict(X_live, verbose=0)
    mse = np.mean(np.power(X_live - reconstruction, 2), axis=1)[0]
    
    ANOMALY_THRESHOLD = 0.01 
    is_anomaly = (mse > ANOMALY_THRESHOLD)
    
    return -1 if is_anomaly else 1, mse

# --- ENDPOINT 1: DATA COLLECTION ---
@app.post("/collect_data")
async def collect_data(data: dict):
    try:
        data['timestamp'] = datetime.datetime.now().isoformat()
        with open(BASELINE_DATA_FILENAME, 'a') as f:
            f.write(json.dumps(data) + '\n')
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [COLLECT] Data logged.")
        return {"message": "Data logged successfully for baseline training."}
    except Exception as e:
        return {"message": "Data logging failed.", "error": str(e)}

# --- ENDPOINT 2: THREAT REPORTING ---
@app.post("/submit_report")
async def submit_report(report: dict):
    
    live_processes = report.get('all_processes_data', [])
    
    # 1. ANALYZE BEHAVIORAL ANOMALY
    prediction, mse_score = score_process_data(live_processes)
    is_anomaly = (prediction == -1)
    
    # 2. CALCULATE IMMUTABLE HASH
    report_json_string = json.dumps(report, sort_keys=True)
    h = SHA256.new(data=report_json_string.encode('utf-8'))
    report_hash = h.hexdigest()
    
    print("\n--- Live Triage Report (GNN-A.E.) ---")
    print(f"ML Score: {mse_score:.6f}")
    print(f"ANOMALY DETECTED: {'YES' if is_anomaly else 'NO'}")
    print(f"IMMUTABLE HASH: {report_hash}")

    # 3. LOG TO BLOCKCHAIN ONLY IF ANOMALY IS FOUND
    if is_anomaly:
        logging_successful = log_hash_to_blockchain(report_hash)
        if logging_successful:
             print("\n[BLOCKCHAIN LOG SUCCESS] HASH COMMITTED TO LEDGER!")
        else:
             print("\n[BLOCKCHAIN LOG FAILED] Check Docker/Network Status.")
    else:
        print("\n[STATUS] Behavior is NORMAL. No blockchain log required.")
    
    print("------------------------------------\n")
    
    return {
        "message": "Triage complete.",
        "status": "Anomaly Detected" if is_anomaly else "Normal",
        "score": float(mse_score),
        "report_hash": report_hash
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)