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

### Core Components

| Directory/File | Description |
|:---------------|:------------|
| `adf_pipelines/` | Azure Data Factory pipeline definitions (4 files) |
| `notebooks/` | Databricks notebooks for data transformation (5 notebooks) |
| `scripts/` | Python utilities and streaming simulation |
| `data/` | Source CSV files (gitignored - download from Kaggle) |
| `samples/` | Sample outputs from Silver and Gold layers |
| `Document/` | Project documentation, reports, and architecture diagrams |
| `screenshots/` | Setup documentation and Power BI visualizations |
| `requirements.txt` | Python dependencies |

### Detailed File Breakdown

**Azure Data Factory Pipelines** (`adf_pipelines/`)
- `adf_pipeline_ingestion.json` - Batch ingestion from Kaggle to Bronze layer
- `pl_master_esports.json` - Master orchestration pipeline
- `pl_transform_silver.json` - Bronze to Silver transformation pipeline
- `pl_aggregate_gold` - Silver to Gold aggregation pipeline

**Databricks Notebooks** (`notebooks/`)
- `setup_connection.ipynb` - Azure Databricks connection and mount setup
- `bronze_to_silver.ipynb` - Data cleaning and Delta table creation
- `silver_to_gold.ipynb` - Aggregation and analytics table creation
- `sql_analysis.ipynb` - SQL queries for insights and analytics
- `04_ml_model.ipynb` - Machine learning model for match outcome prediction

**Scripts** (`scripts/`)
- `stream_simulator.py` - Simulates real-time match data streaming to Azure ADLS Gen2

**Sample Data** (`samples/`)
- `samples_silver/` - 1,000-row samples of cleaned data (matches, players, picks_bans)
- `samples_gold/` - Complete aggregated datasets (player stats, hero stats, daily stats, ML features)

**Documentation** (`Document/`)
- `rapport_final.pdf` - Final project report
- `INF438PdS_G3.pdf` - Project specification document
- `pipeline.png` - Data lakehouse architecture diagram
- `Screenshots/` - Power BI dashboard screenshots and implementation evidence

---

## 🚀 How to Run the Streaming Simulation

This script simulates real-time match data arrival by reading a local CSV and uploading small JSON chunks to the Azure Bronze layer.

### 1. Prerequisites
Ensure you have Python installed and the required libraries:
```bash
pip install azure-storage-file-datalake pandas
```

### 2. Configuration
Open `scripts/stream_simulator.py` and update the following variables with your Azure credentials:

```Python
STORAGE_ACCOUNT_NAME = "sadota2lakehouse"
STORAGE_ACCOUNT_KEY = "xxx"
LOCAL_SOURCE_FILE = "main_metadata.csv"
```

### 3. Execution
Run the script in your terminal:

```Bash
python scripts/stream_simulator.py
```
Expected Output: The console will show "Uploading stream_matches_2025...".

Verification: Go to Azure Portal -> Storage Account -> data/bronze to see the new files appearing in real-time.

## ⚙️ Azure Data Factory Pipeline (Batch Ingestion)
The `adf_pipelines/adf_pipeline_ingestion.json` file contains the definition for the PL_Ingest_Kaggle_To_Bronze pipeline.

**Source:** Local Landing Zone (or Kaggle raw files).

**Destination:** Azure Data Lake Gen2 (bronze/ folder).

**Logic:** Copies all .csv files using a Wildcard path.

To Import this pipeline:

Open Azure Data Factory Studio.

Click New Pipeline -> Import from template/code.

Paste the contents of the JSON file.

## 📊 Sample Data Files (Exemples de fichiers de chaque couche)

CSV sample files from each Lakehouse layer are provided in the `/samples` folder to demonstrate data structure and transformations.

**Silver Layer Samples** (1,000 rows each):
- `silver_cleaned_matches_sample_1000rows_YYYYMMDD.csv`
- `silver_cleaned_players_sample_1000rows_YYYYMMDD.csv`
- `silver_cleaned_picks_bans_sample_1000rows_YYYYMMDD.csv`

**Gold Layer Samples**:
- `gold_player_stats_complete_XXXXrows_YYYYMMDD.csv` (all player stats)
- `gold_hero_stats_complete_XXXrows_YYYYMMDD.csv` (all hero stats)
- `gold_daily_stats_complete_XXXrows_YYYYMMDD.csv` (all daily stats)
- `gold_ml_features_sample_5000rows_YYYYMMDD.csv` (stratified ML sample)

These samples are generated when running notebooks in the `notebooks/` directory (`bronze_to_silver.ipynb` and `silver_to_gold.ipynb`).

---

## 🔄 Data Transformation Workflow

Run notebooks in the following order:

1. `notebooks/setup_connection.ipynb` - Configure Azure storage mount
2. `notebooks/bronze_to_silver.ipynb` - Clean and deduplicate raw data
3. `notebooks/silver_to_gold.ipynb` - Create aggregated analytics tables
4. `notebooks/sql_analysis.ipynb` - Run analytical queries
5. `notebooks/04_ml_model.ipynb` - Train match prediction model

**Power BI Dashboard:** Connect to Gold layer Delta tables or use exported samples from `samples/samples_gold/`

---

## 👥 Team Responsibilities
Member 1 (Infrastructure): Azure Setup, Streaming Script, Batch Ingestion (Bronze).

Member 2 (Data Engineering): Bronze to Silver/Gold Transformation (Databricks/PySpark).

Member 3 (Analytics): SQL Analysis & Power BI Dashboard.

Member 4 (ML & Report): Machine Learning Model & Final Documentation.
