# ☁️ Cloud Budget Tracker (Python + AWS S3)

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)
[![boto3](https://img.shields.io/badge/boto3-SDK-yellow.svg)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A **serverless-style Python project** that securely manages and stores budget data using **AWS S3** as the backend.  
Transactions and category data are saved to S3 in JSON format, while spending reports are generated automatically and uploaded to a separate folder.

---

## 🧠 Overview

**Architecture**
Python CLI ──► AWS S3 (ledger + reports)


- Lightweight CLI app that runs locally or in AWS CloudShell  
- S3 used as persistent storage for all data  
- JSON-based structure for easy reading and portability  
- Secure, versioned, and encrypted data  

---

## ⚙️ Tech Stack

| Component | Description |
|------------|--------------|
| **Python 3.12** | Core logic and budget tracking |
| **boto3** | AWS SDK for S3 interactions |
| **AWS CloudShell** | Cloud execution environment |
| **S3 Bucket** | Secure ledger + report storage |

---

## 💰 Features

- Add, withdraw, and transfer funds between categories  
- Automatically generate **JSON-based spending reports**  
- Store data in **AWS S3** with encryption and versioning  
- Simple CLI interface  
- Easily extendable to **Lambda** or **API Gateway**  

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/elis420/cloud-budget-tracker.git
cd cloud-budget-tracker
```
### 2️⃣ Set up the virtual environment
```bash
python -m venv .venv
source .venv/bin/activate     # Linux/Mac
# OR
.venv\Scripts\activate        # Windows
```
### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```
### 4️⃣ Configure environment variables
```
export BUDGET_BUCKET=elis-budget-tracker-123456
export LEDGER_KEY=data/ledger.json
```
### 5️⃣ Run the app
```bash
python main.py add Food 100 "Initial deposit"
python main.py report
```
## 📊 Example Output

> Report saved to:
```bash
s3://elis-budget-tracker-123456/reports/2025-11-12.json
```
> Sample JSON output:
```json
{
  "Food": 100,
  "Rent": 400,
  "Groceries": 50
}
```

## 🛡️ Security

> All S3 objects are encrypted (SSE-S3) and versioned.
IAM roles follow the principle of least privilege (s3:GetObject, s3:PutObject, s3:ListBucket).
{: .prompt-tip }

🧑‍💻 Author

Elis Cazacu
Cloud Support | Python | AWS | Automation

- 🌐 [Portfolio](https://elis420.github.io)
- 💼 [LinkedIn](https://www.linkedin.com/in/elis-cazacu-b5b823109/)

## 📄 License
This project is licensed under the MIT License — feel free to use, modify, and build upon it.

