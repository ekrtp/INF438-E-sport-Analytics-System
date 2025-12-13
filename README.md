# INF438 - E-sport Analytics System (Dota 2)
Galatasaray University  
**Project:** Advanced Databases (Lakehouse Architecture on Azure)

## 📌 Project Overview
This project implements a Data Lakehouse architecture on Microsoft Azure to analyze Dota 2 E-sports data. The system ingests batch and streaming data into a Bronze layer, transforms it into Silver/Gold layers using Databricks (PySpark), and visualizes insights using Power BI.

**Architecture:**
* **Bronze:** Raw ingestion (Batch from Kaggle + Simulated Streaming).
* **Silver:** Cleaned Delta Tables (Deduplicated, casted).
* **Gold:** Aggregated analytical tables for BI & ML.

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| `stream_simulation.py` | Python script that reads local CSV data and streams it to Azure ADLS Gen2 in mini-batches. |
| `adf_pipeline_ingestion.json` | The Azure Data Factory pipeline code for ingesting historical batch data. |
| `requirements.txt` | Python dependencies required to run the simulation. |

---

## 🚀 How to Run the Streaming Simulation

This script simulates real-time match data arrival by reading a local CSV and uploading small JSON chunks to the Azure Bronze layer.

### 1. Prerequisites
Ensure you have Python installed and the required libraries:
```bash
pip install azure-storage-file-datalake pandas
```

### 2. Configuration
Open stream_simulation.py and update the following variables with your Azure credentials:

```Python
STORAGE_ACCOUNT_NAME = "sadota2lakehouse"
STORAGE_ACCOUNT_KEY = "xxx"
LOCAL_SOURCE_FILE = "main_metadata.csv"
```

### 3. Execution
Run the script in your terminal:

```Bash
python stream_simulation.py
```
Expected Output: The console will show "Uploading stream_matches_2025...".

Verification: Go to Azure Portal -> Storage Account -> data/bronze to see the new files appearing in real-time.

##⚙️ Azure Data Factory Pipeline (Batch Ingestion)
The adf_pipeline_ingestion.json file contains the definition for the PL_Ingest_Kaggle_To_Bronze pipeline.

Source: Local Landing Zone (or Kaggle raw files).

Destination: Azure Data Lake Gen2 (bronze/ folder).

Logic: Copies all .csv files using a Wildcard path.

To Import this pipeline:

Open Azure Data Factory Studio.

Click New Pipeline -> Import from template/code.

Paste the contents of the JSON file.

## 👥 Team Responsibilities
Member 1 (Infrastructure): Azure Setup, Streaming Script, Batch Ingestion (Bronze).

Member 2 (Data Engineering): Bronze to Silver/Gold Transformation (Databricks/PySpark).

Member 3 (Analytics): SQL Analysis & Power BI Dashboard.

Member 4 (ML & Report): Machine Learning Model & Final Documentation.
