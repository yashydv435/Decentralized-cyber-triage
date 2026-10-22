🌐 Decentralized Behavioral Cyber Triage Tool
AI + Blockchain Powered Zero-Day Threat Detection & Tamper-Proof Forensics
<p align="center"> <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge"> <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge"> <img src="https://img.shields.io/badge/TensorFlow-Autoencoder-orange?style=for-the-badge"> <img src="https://img.shields.io/badge/Hyperledger-Fabric-red?style=for-the-badge"> <img src="https://img.shields.io/badge/Architecture-Decentralized-black?style=for-the-badge"> </p>
🚀 Overview

Modern cyber-attacks—especially zero-day exploits, fileless malware, and stealthy process injections—cannot be detected using traditional antivirus solutions.

This project solves that problem by integrating:

✔ AI-based Behavioral Anomaly Detection
✔ Graph Neural Networks (GNN Autoencoders)
✔ Immutable Blockchain Logging (Hyperledger Fabric)
✔ Decentralized Triage & Evidence Preservation

Whenever any suspicious behaviour is detected, the system:

Generates a forensic report

Computes its SHA-256 immutable hash

Stores the hash on a tamper-proof blockchain, ensuring the evidence cannot be altered

This creates an enterprise-grade, tamper-proof, real-time cyber-triage solution.

🧠 Features
🔍 1. AI-Powered Anomaly Detection

Uses Graph-based Autoencoder (GNN A.E.)

Detects abnormal system process behaviour

Works even for unknown / zero-day attacks

🔗 2. Blockchain-based Forensic Logging

Hash is committed to Hyperledger Fabric

Ensures immutability, auditability, and non-repudiation

Attackers cannot modify logs

⚡ 3. Real-time Backend (FastAPI)

Lightweight, fast, asynchronous REST server

Handles triage reports from multiple agents

🔐 4. Decentralized Trust Model

No central server controlling forensic records

Organizations can share evidence securely

📦 5. Modular Architecture

Agent → Server → ML Engine → Blockchain

Works standalone or integrates with existing SIEM/SOAR

🏗️ Architecture
┌──────────┐       ┌──────────────┐       ┌───────────────────┐       ┌────────────────────────┐
│  Agent   │  ⇒    │   API Server │  ⇒    │  ML Anomaly Model │  ⇒    │ Hyperledger Fabric Peer │
└──────────┘       └──────────────┘       └───────────────────┘       └────────────────────────┘
     │                     │                       │                             │
Collects live        Receives triage          GNN Autoencoder                Commits SHA256
process telemetry     reports via REST         scores behavior               hash to blockchain

🛠️ Tech Stack
Component	Technology
Agent	Python + psutil
Backend API	FastAPI
ML Engine	TensorFlow (Autoencoder) / PyTorch Geometric
Blockchain	Hyperledger Fabric
Hashing	SHA-256 (PyCryptodome)
Environment	Ubuntu / Docker / WSL2
Off-chain Storage (optional)	MinIO / S3
📥 Installation & Setup
1️⃣ Clone the repo
git clone https://github.com/yashydv435/Decentralized-cyber-triage.git
cd Decentralized-cyber-triage

2️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Start FastAPI backend
uvicorn server:app --reload --host 0.0.0.0 --port 8000

5️⃣ Run agent script
python agent.py

6️⃣ Submit test triage report
curl -X POST "http://localhost:8000/submit_report" -H "Content-Type: application/json" -d '{"all_processes_data": []}'

🔐 Blockchain Logging (Hyperledger Fabric)

To commit forensic report hashes to the ledger:

Start Fabric Test Network

Ensure peer0.org1.example.com container is running

Server automatically detects anomaly and logs hash

Typical triage output:

--- Live Triage Report (GNN-A.E.) ---
ML Score: 5.3341
ANOMALY DETECTED: YES
HASH: d3f447...8e19f

[BLOCKCHAIN LOG SUCCESS] HASH COMMITTED TO LEDGER!

📊 Results

Successfully detects anomalous process behaviour

Logs cannot be modified once stored on blockchain

Real-time threat triage via API

Works even without signature databases

Resilient against log tampering, deletion and timestamp forgery

📌 Project Structure
📁 decentralized-cyber-triage/
 ┣ 📁 server/            → FastAPI backend & ML scoring
 ┣ 📁 agent/             → Endpoint agent
 ┣ 📁 fabric-samples/    → Hyperledger Fabric network (local)
 ┣ 📄 gnn_baseline_data.json
 ┣ 📄 train_gnn.py       → ML training script
 ┣ 📄 server.py          → API server entry
 ┣ 📄 agent.py           → Telemetry collector
 ┣ 📄 README.md
 ┗ 📄 .gitignore

🚀 Future Enhancements

Real malware dataset integration

Kubernetes-based scalable deployment

Real-time dashboards (Grafana)

Multi-organization Fabric channels

SIEM/SOAR integration

Advanced GNN models: GAT, GraphSAGE, GCN

🤝 Contributing

Contributions are welcome!
Please open a pull request or create an issue before starting major changes.

📄 License

This project is licensed under the MIT License.

💬 Contact

For queries or collaboration:
📧 yasyaadav@gmail.com

🔥 Developed with passion for Cybersecurity + AI + Blockchain.
