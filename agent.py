import psutil
import requests
import json
import socket
import time
import sys
import datetime

# --- CONFIGURATION ---
# IMPORTANT: Use your Main PC's Host-Only IP (e.g., 192.168.173.1)
MAIN_PC_IP = "http://192.168.173.1:8000"

COLLECTION_URL = f"{MAIN_PC_IP}/collect_data"
REPORTING_URL = f"{MAIN_PC_IP}/submit_report"

# --- PROCESS DEFINITIONS ---
malicious_processes = ["python.exe"] 

# --- DATA COLLECTION ---
def get_process_data():
    all_processes_data = []
    for process in psutil.process_iter(['name', 'pid', 'username', 'ppid']):
        try:
            process_info = {
                'pid': process.info['pid'],
                'ppid': process.info['ppid'],
                'name': process.info['name'],
                'username': process.info['username'],
            }
            all_processes_data.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return all_processes_data

def send_data(url, data_payload):
    try:
        response = requests.post(url, json=data_payload, timeout=10)
        return response.json()
    except requests.exceptions.ConnectionError:
        print(f"[{time.strftime('%H:%M:%S')}] ERROR: Connection Failed to Server at {url}.")
        return {"message": "Connection Failed."}

def run_data_collection_mode():
    print(f"--- Starting GNN Data Collection to {COLLECTION_URL} ---")
    while True:
        data_payload = {
            "device_name": socket.gethostname(), 
            "local_ip": socket.gethostbyname(socket.gethostname()),
            "processes": get_process_data()
        }
        response = send_data(COLLECTION_URL, data_payload)
        print(f"[{time.strftime('%H:%M:%S')}] Data sent. Response: {response.get('message')}")
        time.sleep(30) 

def run_final_triage_mode():
    print("--- Running Final Triage Scan ---")
    all_processes_data = get_process_data()
    
    threats_found = []
    for process in all_processes_data:
        if process['name'] in malicious_processes:
            threats_found.append({
                'pid': process['pid'],
                'name': 'MALWARE.EXE (Detected Python Process)', 
                'original_name': process['name'],
                'username': process['username'],
            })

    report = {
        "device_name": socket.gethostname(), 
        "local_ip": socket.gethostbyname(socket.gethostname()),
        "scan_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "all_processes_data": all_processes_data, 
        "detected_threats": threats_found,
    }
    
    # Send to the REPORTING URL (where ML analysis happens)
    try:
        response = requests.post(REPORTING_URL, json=report, timeout=10)
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"\n--- Live Triage Report ---")
            print(f"Device: {report['device_name']}")
            print(f"ML Score: {response_data.get('score', 'N/A')}") 
            print(f"ANOMALY DETECTED: {'YES' if response_data.get('status') == 'Anomaly Detected' else 'NO'}")
            print(f"IMMUTABLE HASH: {response_data.get('report_hash', 'N/A')[:15]}...")
            print(f"[STATUS] Behavior is {'ANOMALOUS' if response_data.get('status') == 'Anomaly Detected' else 'NORMAL'}.")
        else:
            print(f"\n[ERROR] Server returned HTTP Status Code: {response.status_code}")
            print(f"Server responded with text: {response.text[:100]}...") 
            
    except requests.exceptions.ConnectionError:
        print(f"\n[ERROR] Connection Failed. Server is not running at {REPORTING_URL}.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "REPORT":
        run_final_triage_mode()
    else:
        run_data_collection_mode()