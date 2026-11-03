# Insurance Claims Data Warehouse with GenAI

## 1. Project Overview

The **Insurance Claims Data Warehouse** is an end-to-end data engineering project that processes insurance data, transforms it into analytics-ready datasets, stores it in AWS, and provides business insights through SQL queries and an interactive dashboard.

The project also integrates Generative AI to summarize insurance claim notes and help users understand important observations about a claim.

The project follows the **Medallion Architecture**:

- **Bronze Layer:** Stores the original raw data.
- **Silver Layer:** Stores cleaned and transformed data.
- **Gold Layer:** Stores aggregated, business-ready datasets.

### Main objectives

1. Ingest insurance data from CSV files.
2. Store structured data in MySQL.
3. Perform data validation and quality checks.
4. Process and transform data using PySpark.
5. Build Bronze, Silver, and Gold data layers.
6. Store processed datasets in Amazon S3.
7. Register Gold datasets in the AWS Glue Data Catalog.
8. Run analytical SQL queries using Amazon Athena.
9. Generate AI summaries of claim notes using Ollama Cloud.
10. Build an interactive dashboard using Streamlit.

**Dataset note:** The project uses a synthetic insurance claims dataset for learning and demonstration. It does not contain real customer insurance records.

---

## 2. Technologies Used and Why We Use Them

| Technology | Purpose |
|---|---|
| Python | CSV ingestion, validation, and application logic |
| Pandas | Reading and exploring CSV files |
| MySQL | Relational database and structured data storage |
| SQL | Data validation and business analytics |
| SQLAlchemy | Connecting Python to MySQL |
| PySpark | Distributed-style data processing and transformations |
| Parquet | Efficient columnar storage for analytics |
| AWS S3 | Cloud storage for Bronze, Silver, and Gold data |
| AWS Glue Data Catalog | Stores metadata and table definitions |
| Amazon Athena | Runs SQL queries directly on S3 data |
| Ollama Cloud | Generates AI-powered claim note summaries |
| Streamlit | Builds the interactive frontend |
| Plotly | Creates interactive charts |
| Git | Version control |
| VS Code | Main development environment |
| Ubuntu WSL2 | Runs PySpark in a Linux environment on Windows |

### Why use these technologies?

- **MySQL:** Stores structured relational data and supports primary keys, foreign keys, and SQL queries.
- **Python:** Automates data loading and connects different parts of the project.
- **PySpark:** Cleans, joins, groups, and aggregates datasets efficiently.
- **Parquet:** Stores analytics data in a compressed columnar format.
- **S3:** Provides scalable cloud object storage.
- **Glue Data Catalog:** Makes datasets discoverable as tables.
- **Athena:** Allows SQL analytics without managing a database server.
- **Ollama Cloud:** Adds a GenAI feature that summarizes unstructured claim notes.
- **Streamlit:** Makes project results accessible through a web dashboard.

---

## 3. Project Architecture

```text
                  INSURANCE CSV DATA
                          |
                          v
                 Python Data Ingestion
                          |
             +------------+------------+
             |                         |
             v                         v
        MySQL Database             S3 Bronze
             |                         |
             |                         v
             |                  PySpark Cleaning
             |                         |
             |                         v
             |                     S3 Silver
             |                         |
             |                         v
             |                  PySpark Aggregation
             |                         |
             |                         v
             |                      S3 Gold
             |                         |
             |                         v
             |                 Glue Data Catalog
             |                         |
             |                         v
             |                    Athena SQL
             |                         |
             +------------+------------+
                          |
                          v
                 Business Analytics
                          |
             +------------+------------+
             |                         |
             v                         v
        Streamlit Dashboard       Ollama Cloud
             |                         |
             v                         v
       Interactive Charts       AI Claim Summaries
```

---

## 4. Project Folder Structure

```text
HCL_Insurance_Claims_Project/
│
├── .env
├── .gitignore
├── .venv/
├── .venv-linux/
│
├── data/
│   ├── raw/
│   │   ├── policies.csv.csv
│   │   ├── beneficiaries.csv.csv
│   │   ├── claims.csv.csv
│   │   ├── claims_fraud.csv.csv
│   │   └── claims_notes.csv.csv
│   │
│   ├── processed/
│   │   ├── policies/
│   │   ├── beneficiaries/
│   │   ├── claims/
│   │   ├── claims_fraud/
│   │   └── claims_notes/
│   │
│   └── gold/
│       ├── claim_summary/
│       ├── policy_analysis/
│       └── fraud_analysis/
│
├── mysql/
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   └── 03_validate_tables.sql
│
├── python/
│   ├── 01_data_exploration.py
│   ├── 02_generate_schema_report.py
│   ├── 03_load_csv_to_mysql.py
│   ├── 04_claim_ai_summarizer.py
│   └── 05_analyze_claim.py
│
├── pyspark/
│   ├── 01_read_csv.py
│   ├── 02_clean_transform.py
│   └── 03_create_gold.py
│
├── aws/
│
├── reports/
│   ├── data_exploration_notes.md
│   ├── schema_report.md
│   └── architecture.md
│
├── app.py
├── README.md
└── requirements.txt
```

### Folder explanation

- `data/raw/`: Original CSV files. These are not directly modified by the transformation process.
- `data/processed/`: Cleaned datasets produced by PySpark. These represent the Silver layer.
- `data/gold/`: Aggregated datasets produced by PySpark for business analytics.
- `mysql/`: SQL scripts for database creation, table creation, and validation.
- `python/`: Python scripts for exploration, schema reporting, MySQL loading, and AI analysis.
- `pyspark/`: Scripts for reading, cleaning, transforming, and aggregating data.
- `aws/`: Space for AWS-related scripts and documentation.
- `reports/`: Project documentation and data-quality reports.
- `app.py`: Streamlit frontend application.
- `.env`: Stores private configuration such as the Ollama API key.
- `.gitignore`: Prevents private files and generated environments from being committed to Git.

---

## 5. Dataset Description

The project uses five CSV files.

| Dataset | Records | Description |
|---|---:|---|
| policies | 50 | Insurance policy information |
| beneficiaries | 100 | Policy beneficiary information |
| claims | 100 | Insurance claim information |
| claims_fraud | 102 | Fraud investigation information |
| claims_notes | 238 | Notes recorded against claims |
| **Total** | **590** | **All source records** |

### Relationships between datasets

```text
policies
   |
   | policy_id
   |
   +---------- beneficiaries

   |
   | policy_id
   |
   +---------- claims
                  |
                  | claim_id
                  |
                  +---------- claims_fraud
                  |
                  +---------- claims_notes
```

### Important data-quality observations

The original dataset contains missing values:

- 73 missing claim amounts.
- 49 missing beneficiary names.
- 9 missing beneficiary relationships.
- 7 policies without an end date.
- 5 claims without an updated date.

These values are checked and handled according to the transformation logic. Missing values are not automatically replaced with zero because that could change the business meaning of the data.

---

## 6. Software Prerequisites

Install or configure the following:

1. Windows 11.
2. Visual Studio Code.
3. Python.
4. MySQL Server 8.0.
5. Java 17 or later for the installed Spark version.
6. Ubuntu through WSL2.
7. AWS account with access to S3, Glue Data Catalog, and Athena.
8. Ollama Cloud API key.

### VS Code extensions

Recommended extensions:

- Python
- Jupyter
- SQLTools
- SQLTools MySQL/MariaDB/TiDB Driver

---

## 7. Initial Project Setup

### Step 1: Open the project in VS Code

Open the project folder:

```text
HCL_Insurance_Claims_Project
```

Open the integrated terminal:

```text
Terminal > New Terminal
```

For Windows-based Python scripts and Streamlit, use **PowerShell**.

For PySpark scripts, use **Ubuntu WSL**.

### Step 2: Create the Windows virtual environment

Run in PowerShell from the project root:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

The terminal should show:

```text
(.venv)
```

Why use a virtual environment?

It keeps project dependencies separate from other Python projects.

### Step 3: Install Python dependencies

Run:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you need to install the packages individually:

```powershell
pip install pandas
pip install sqlalchemy
pip install pymysql
pip install streamlit
pip install plotly
pip install pyarrow
pip install ollama
pip install python-dotenv
```

Why these packages?

- `pandas`: CSV reading and data exploration.
- `sqlalchemy`: Database connection management.
- `pymysql`: MySQL database driver.
- `streamlit`: Frontend dashboard.
- `plotly`: Interactive charts.
- `pyarrow`: Parquet support for Pandas.
- `ollama`: Ollama API client.
- `python-dotenv`: Loads private settings from `.env`.

### Step 4: Verify the installed packages

```powershell
python --version
pip list
```

---

## 8. MySQL Database Setup

### Why MySQL?

MySQL stores the structured insurance datasets in relational tables. It allows us to maintain relationships between policies, beneficiaries, claims, and investigations.

### Step 1: Start MySQL Server

On Windows, open PowerShell and run:

```powershell
Get-Service MySQL80
```

If it is stopped:

```powershell
Start-Service MySQL80
```

### Step 2: Connect to MySQL

Run:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Enter your MySQL password when prompted. Do not put the password directly in the command.

### Step 3: Create the database

Open:

```text
mysql/01_create_database.sql
```

Execute:

```sql
CREATE DATABASE IF NOT EXISTS insurance_claims_db;
USE insurance_claims_db;
```

### Step 4: Create the tables

Open:

```text
mysql/02_create_tables.sql
```

The script creates five relational tables:

1. policies
2. beneficiaries
3. claims
4. claims_fraud
5. claims_notes

It also defines primary keys and foreign key relationships.

Execute the SQL script from the project root after connecting to MySQL:

```sql
SOURCE mysql/02_create_tables.sql;
```

### Step 5: Verify tables

```sql
USE insurance_claims_db;

SHOW TABLES;
```

Expected tables:

```text
policies
beneficiaries
claims
claims_fraud
claims_notes
```

---

## 9. Python Data Exploration

### Why perform data exploration?

Before loading data into a database, we need to understand:

- Number of records.
- Number of columns.
- Data types.
- Missing values.
- Duplicate records.
- Dataset structure.

### Step 1: Run the exploration script

In PowerShell, with `.venv` activated:

```powershell
python python/01_data_exploration.py
```

### Step 2: Generate the schema report

```powershell
python python/02_generate_schema_report.py
```

The report is saved in:

```text
reports/schema_report.md
```

This report helps us understand the source data before transformation.

---

## 10. Load CSV Data into MySQL

### Why use Python for loading?

Instead of manually importing every CSV, Python automates the process and performs validation before inserting records.

The loading script:

- Finds the five CSV files.
- Checks expected columns.
- Converts date values.
- Handles null values.
- Checks primary-key uniqueness.
- Checks required foreign-key fields.
- Inserts the data into MySQL.

### Step 1: Run the loader

Make sure MySQL is running.

Run in PowerShell:

```powershell
python python/03_load_csv_to_mysql.py
```

Enter your MySQL password when prompted.

The script loads all five CSV datasets into the corresponding tables.

**Important:** The loader checks whether the tables already contain data to prevent accidental duplicate loading. Do not rerun it against populated tables without understanding the script's reload protection.

### Step 2: Validate the record counts

Open:

```text
mysql/03_validate_tables.sql
```

Execute:

```sql
SOURCE mysql/03_validate_tables.sql;
```

Expected record counts:

| Table | Expected records |
|---|---:|
| policies | 50 |
| beneficiaries | 100 |
| claims | 100 |
| claims_fraud | 102 |
| claims_notes | 238 |

Total: 590 records.

### Step 3: Run data-quality checks

The existing validation SQL file also includes checks for:

- Missing claim amounts.
- Missing beneficiary names.
- Missing relationships.
- Missing policy end dates.
- Missing claim updated dates.
- Orphan claim records.
- Orphan fraud records.

An orphan record is a record whose referenced parent record does not exist.

The project validation found zero orphan claims and zero orphan fraud records.

### Step 4: Run business analytics queries

The SQL validation file also includes analytics such as:

- Claim count by status.
- Fraud investigation outcomes.
- Total claim amount by policy type.

These queries demonstrate how relational SQL can be used to answer business questions.

---

## 11. PySpark Environment Setup Using Ubuntu WSL2

### Why use PySpark?

PySpark is used for data transformation and aggregation. It can process large datasets using distributed computing concepts.

We use Ubuntu WSL2 because the Windows Spark environment encountered Hadoop native binary configuration problems. The Linux environment provides a more straightforward setup for running the installed Spark version.

### Step 1: Open Ubuntu

Open Ubuntu from the Windows Start menu.

### Step 2: Navigate to the project folder

Run:

```bash
cd "/mnt/c/Users/Ashish yadav/OneDrive/Desktop/HCL_Insurance_Claims_Project"
```

This path maps the Windows project folder into Ubuntu.

### Step 3: Create the Linux virtual environment

This environment is separate from the Windows `.venv`.

```bash
python3 -m venv .venv-linux
```

### Step 4: Activate the Linux environment

```bash
source .venv-linux/bin/activate
```

The terminal should show:

```text
(.venv-linux)
```

### Step 5: Install PySpark

```bash
python -m pip install --upgrade pip
pip install pyspark
```

### Step 6: Verify Java

The installed Spark version requires Java 17 or later.

```bash
java -version
```

If Java 17 is not installed:

```bash
sudo apt update
sudo apt install openjdk-17-jdk -y
```

Select Java 17 if multiple versions are installed:

```bash
sudo update-alternatives --config java
sudo update-alternatives --config javac
```

Verify again:

```bash
java -version
javac -version
```

### Why do we need Java?

Apache Spark runs on the Java Virtual Machine (JVM). PySpark uses Python to interact with Spark, while Spark's execution engine relies on the JVM.

---

## 12. Run PySpark Data Processing

Run all three scripts from the project root in Ubuntu with `.venv-linux` activated.

### Step 1: Read raw CSV files

```bash
python pyspark/01_read_csv.py
```

Purpose:

- Read the original CSV datasets.
- Create Spark DataFrames.
- Inspect the schema and records.
- Understand how Spark reads the source data.

### Step 2: Clean and transform data

```bash
python pyspark/02_clean_transform.py
```

Purpose:

- Clean source datasets.
- Handle missing and inconsistent values according to the transformation rules.
- Convert columns into appropriate data types.
- Prepare cleaned datasets for analytics.
- Write the results in Parquet format.

Output:

```text
data/processed/
```

This represents the **Silver Layer**.

### Step 3: Create Gold datasets

```bash
python pyspark/03_create_gold.py
```

Purpose:

- Group claims by status.
- Calculate total and average claim amounts.
- Count missing claim amounts.
- Analyze claims by policy type.
- Aggregate fraud investigations by fraud type and outcome.

Output:

```text
data/gold/
```

The three Gold datasets are:

```text
data/gold/
├── claim_summary/
├── policy_analysis/
└── fraud_analysis/
```

### What is Parquet?

Parquet is a columnar file format optimized for analytical workloads. It supports efficient reading of selected columns and is commonly used in data lake architectures.

### Medallion architecture summary

| Layer | Location | Purpose |
|---|---|---|
| Bronze | S3 raw data | Original source data |
| Silver | S3 processed data | Cleaned and transformed data |
| Gold | S3 gold data | Business-ready aggregates |

---

## 13. AWS Cloud Setup

### Why AWS?

AWS is used to demonstrate how a data warehouse can operate using cloud storage, metadata management, and serverless SQL analytics.

The project uses:

- Amazon S3
- AWS Glue Data Catalog
- Amazon Athena

### AWS configuration

| Setting | Value |
|---|---|
| AWS Region | ap-southeast-2 |
| Region name | Asia Pacific (Sydney) |
| S3 bucket | hcl-insurance-claims-1 |
| Glue database | insurance_claims_catalog |
| Athena result location | s3://hcl-insurance-claims-1/athena-results/ |

### Step 1: Create the S3 bucket

In the AWS Console:

1. Open Amazon S3.
2. Create a bucket named `hcl-insurance-claims-1`.
3. Select region `ap-southeast-2`.
4. Keep public access blocked.
5. Create the bucket.

The bucket contains these logical folders:

```text
hcl-insurance-claims-1/
│
├── bronze/
├── silver/
├── gold/
│   ├── claim_summary/
│   ├── policy_analysis/
│   └── fraud_analysis/
│
└── athena-results/
```

### Step 2: Upload Bronze data

Upload the original CSV files from:

```text
data/raw/
```

to:

```text
s3://hcl-insurance-claims-1/bronze/
```

### Step 3: Upload Silver data

Upload the processed Parquet datasets from:

```text
data/processed/
```

to the corresponding folders under:

```text
s3://hcl-insurance-claims-1/silver/
```

### Step 4: Upload Gold data

Upload the three Gold Parquet datasets from:

```text
data/gold/
```

to:

```text
s3://hcl-insurance-claims-1/gold/
```

### Optional: Upload using AWS CLI

If AWS CLI is installed and configured, the following commands can be run from the project root in PowerShell.

Check AWS CLI:

```powershell
aws --version
```

Configure credentials if needed:

```powershell
aws configure
```

Enter credentials securely into the CLI prompts. Never paste access keys or passwords into project files or public repositories.

Set the region to:

```text
ap-southeast-2
```

Upload Bronze:

```powershell
aws s3 sync data/raw/ s3://hcl-insurance-claims-1/bronze/ --region ap-southeast-2
```

Upload Silver:

```powershell
aws s3 sync data/processed/ s3://hcl-insurance-claims-1/silver/ --region ap-southeast-2
```

Upload Gold:

```powershell
aws s3 sync data/gold/ s3://hcl-insurance-claims-1/gold/ --region ap-southeast-2
```

Verify uploaded files:

```powershell
aws s3 ls s3://hcl-insurance-claims-1/ --recursive
```

The AWS Console upload method can also be used if AWS CLI is not configured.

**Note:** The AWS CLI commands are optional alternatives to the successful Console uploads. Do not upload duplicate copies into different folder structures.

---

## 14. AWS Glue Data Catalog

### Why Glue Data Catalog?

Amazon S3 stores the actual files, but Athena needs table metadata to understand their structure.

Glue Data Catalog stores:

- Database names.
- Table names.
- Column names.
- Data types.
- S3 storage locations.
- File format information.

### Step 1: Create a Glue database

Open AWS Glue.

Create the database:

```text
insurance_claims_catalog
```

### Step 2: Register Gold tables

The Glue crawler could not be created because of an AWS account access restriction.

Instead, the project manually registered the three Gold tables through Athena DDL statements. Athena created the external table definitions in the Glue Data Catalog.

A crawler is therefore not required for the current project.

The three registered tables are:

```text
claim_summary
policy_analysis
fraud_analysis
```

---

## 15. Amazon Athena SQL Analytics

### Why Athena?

Amazon Athena allows SQL queries directly on data stored in Amazon S3. It does not require us to run or maintain a database server for these analytics.

### Step 1: Open Athena

1. Open Amazon Athena in the AWS Console.
2. Select the database `insurance_claims_catalog`.
3. Configure the query result location:

```text
s3://hcl-insurance-claims-1/athena-results/
```

### Step 2: Create the claim summary table

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS claim_summary (
    status STRING,
    total_claims BIGINT,
    total_claim_amount DECIMAL(22,2),
    average_claim_amount DECIMAL(22,2),
    missing_amount_count BIGINT
)
STORED AS PARQUET
LOCATION 's3://hcl-insurance-claims-1/gold/claim_summary/';
```

### Step 3: Create the policy analysis table

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS policy_analysis (
    policy_type STRING,
    total_claims BIGINT,
    total_claim_amount DECIMAL(22,2),
    average_claim_amount DECIMAL(22,2)
)
STORED AS PARQUET
LOCATION 's3://hcl-insurance-claims-1/gold/policy_analysis/';
```

### Step 4: Create the fraud analysis table

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS fraud_analysis (
    fraud_type STRING,
    outcome STRING,
    total_investigations BIGINT
)
STORED AS PARQUET
LOCATION 's3://hcl-insurance-claims-1/gold/fraud_analysis/';
```

### Step 5: Validate the tables

```sql
SHOW TABLES IN insurance_claims_catalog;
```

Preview the data:

```sql
SELECT * FROM claim_summary;
```

```sql
SELECT * FROM policy_analysis;
```

```sql
SELECT * FROM fraud_analysis;
```

### Step 6: Business analytics queries

**A. Claims by status**

```sql
SELECT
    status,
    total_claims,
    total_claim_amount,
    average_claim_amount,
    missing_amount_count
FROM claim_summary
ORDER BY total_claims DESC;
```

**B. Claims by policy type**

```sql
SELECT
    policy_type,
    total_claims,
    total_claim_amount,
    average_claim_amount
FROM policy_analysis
ORDER BY total_claim_amount DESC;
```

**C. Fraud investigation outcomes**

```sql
SELECT
    fraud_type,
    outcome,
    SUM(total_investigations) AS total_investigations
FROM fraud_analysis
GROUP BY fraud_type, outcome
ORDER BY total_investigations DESC;
```

**D. Total claims**

```sql
SELECT SUM(total_claims) AS total_claims
FROM claim_summary;
```

**E. Overall missing claim amounts**

```sql
SELECT SUM(missing_amount_count) AS missing_amounts
FROM claim_summary;
```

These queries demonstrate how Gold datasets can support business reporting and decision-making.

**AWS cost note:** Athena charges based on the amount of data scanned. Use focused queries and avoid repeatedly scanning large datasets. Do not create unnecessary AWS resources or scheduled crawlers.

---

## 16. GenAI Integration Using Ollama Cloud

### Why add GenAI?

Insurance claim notes contain unstructured text. Reading many notes manually can take time.

The GenAI feature summarizes claim notes and highlights important observations.

The AI assistant is designed to support human review. It does not make final insurance decisions.

### Step 1: Configure the environment file

Open the root-level file:

```text
.env
```

Add your own Ollama Cloud credentials:

```env
OLLAMA_API_KEY=YOUR_OLLAMA_API_KEY
OLLAMA_MODEL=YOUR_SUPPORTED_OLLAMA_MODEL
```

Replace the placeholders with your actual credentials and a model available to your Ollama account.

**Never share the actual API key or commit `.env` to Git.**

### Step 2: Check `.gitignore`

The root `.gitignore` should include:

```gitignore
.env
.venv/
.venv-linux/
__pycache__/
*.pyc
```

This prevents private credentials and local Python environments from being committed.

### Step 3: Run the AI summarizer test

In PowerShell with `.venv` activated:

```powershell
python python/04_claim_ai_summarizer.py
```

This tests the basic AI summarization functionality.

### Step 4: Run AI analysis using actual claim notes

```powershell
python python/05_analyze_claim.py
```

Enter a claim ID when prompted.

The script:

1. Reads claim notes from the source CSV.
2. Finds notes associated with the selected claim.
3. Combines the notes into a prompt.
4. Sends the prompt to Ollama Cloud.
5. Displays the AI-generated analysis.

### AI output limitations

- AI summaries can contain mistakes.
- The output is not a verified fraud finding.
- The output is not a final claim approval or rejection.
- Human review is required before any business decision.

---

## 17. Streamlit Frontend

### Why Streamlit?

Streamlit allows us to build an interactive Python-based web application without creating a separate frontend framework.

The application provides three pages.

### Page 1: Dashboard

Displays:

- Total claims.
- Approved claims.
- Denied claims.
- Approval percentage.
- Claims by status.
- Policy analysis.
- Fraud investigation analysis.
- Missing claim amount information.

### Page 2: Claim Details Explorer

Allows the user to:

- Select a claim ID.
- View its associated notes.
- See the number of notes.
- Download selected claim notes as a CSV file.

### Page 3: AI Claims Assistant

Allows the user to:

- Select a claim ID.
- Retrieve its claim notes.
- Generate an AI-powered summary.
- Review important observations from the notes.

### Step 1: Open PowerShell

Navigate to the project root if needed:

```powershell
cd "C:\Users\Ashish yadav\OneDrive\Desktop\HCL_Insurance_Claims_Project"
```

### Step 2: Activate the Windows environment

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Run Streamlit

```powershell
python -m streamlit run app.py
```

### Step 4: Open the application

Open the URL displayed in the terminal. Usually:

```text
http://localhost:8501
```

### Step 5: Stop the application

Return to the terminal and press:

```text
Ctrl + C
```

---

## 18. Complete Commands to Run the Project Again

This section is the quick reference for running the completed project.

### A. Start MySQL

In Windows PowerShell:

```powershell
Start-Service MySQL80
```

### B. Run Python scripts

Activate the Windows environment:

```powershell
.venv\Scripts\Activate.ps1
```

Run exploration:

```powershell
python python/01_data_exploration.py
```

Generate the schema report:

```powershell
python python/02_generate_schema_report.py
```

Load CSV data into MySQL:

```powershell
python python/03_load_csv_to_mysql.py
```

Run the AI summarizer test:

```powershell
python python/04_claim_ai_summarizer.py
```

Analyze an actual claim:

```powershell
python python/05_analyze_claim.py
```

**Important:** The database loader is intended for initial loading. It will not load the same data again when the target tables are already populated.

### C. Run PySpark scripts

Open Ubuntu and navigate to the project:

```bash
cd "/mnt/c/Users/Ashish yadav/OneDrive/Desktop/HCL_Insurance_Claims_Project"
```

Activate the Linux environment:

```bash
source .venv-linux/bin/activate
```

Read raw data:

```bash
python pyspark/01_read_csv.py
```

Clean and transform:

```bash
python pyspark/02_clean_transform.py
```

Create Gold datasets:

```bash
python pyspark/03_create_gold.py
```

### D. Run the Streamlit application

Return to Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Run:

```powershell
python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

### E. Run AWS analytics

AWS resources are already configured for this project.

Open Athena in the AWS Console, select:

```text
Database: insurance_claims_catalog
```

Run the saved or documented SQL queries against:

```text
claim_summary
policy_analysis
fraud_analysis
```

You do not need to rerun the entire AWS setup every time you start the local application.

---

## 19. Important Troubleshooting

### Problem 1: Python command not found

Check:

```powershell
python --version
```

If Python is installed but not recognized, verify the Python installation and PATH configuration.

### Problem 2: Virtual environment activation fails

In PowerShell, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate:

```powershell
.venv\Scripts\Activate.ps1
```

### Problem 3: MySQL connection error

Check whether the service is running:

```powershell
Get-Service MySQL80
```

Start it if necessary:

```powershell
Start-Service MySQL80
```

Verify the database name and credentials.

### Problem 4: PySpark Java error

Check:

```bash
java -version
```

Make sure Java 17 or later is selected for the installed Spark version.

Also confirm that `.venv-linux` is activated.

### Problem 5: PySpark cannot find CSV files

Check that you are running commands from the project root and that all five CSV files exist in:

```text
data/raw/
```

### Problem 6: Streamlit cannot find Gold datasets

Run the PySpark scripts first:

```bash
python pyspark/01_read_csv.py
python pyspark/02_clean_transform.py
python pyspark/03_create_gold.py
```

Confirm that the three folders exist under:

```text
data/gold/
```

### Problem 7: Ollama API error

Check:

- The `.env` file exists in the project root.
- The API key is valid.
- The model name is supported by your account.
- The internet connection is working.

Never print or share the actual API key when troubleshooting.

### Problem 8: Athena returns no records

Check:

- The Gold Parquet files exist in the correct S3 locations.
- The Athena table locations match the S3 paths.
- The Glue database is selected.
- The table definitions match the Parquet column structure.

---

## 20. Key Project Results

The project successfully demonstrates:

- Ingestion of 590 source records across five datasets.
- Relational database creation in MySQL.
- Data-quality validation and relationship checks.
- PySpark-based data cleaning and transformation.
- Bronze, Silver, and Gold data organization.
- Parquet-based analytical datasets.
- Cloud storage using Amazon S3.
- Manual table registration in AWS Glue Data Catalog.
- SQL analytics using Amazon Athena.
- AI-based claim note summarization using Ollama Cloud.
- Interactive frontend using Streamlit and Plotly.

---

## 21. What I Learned from This Project

### Data Engineering

- Data ingestion.
- Data cleaning.
- Data validation.
- Relational database design.
- Primary keys and foreign keys.
- ETL pipeline development.
- Medallion architecture.
- Batch data processing.
- Parquet storage.

### SQL and Analytics

- Database and table creation.
- Joins.
- Grouping and aggregation.
- NULL handling.
- Data-quality queries.
- Business analytics.

### Big Data

- Spark DataFrames.
- PySpark transformations.
- GroupBy and aggregation.
- DataFrame joins.
- Writing Parquet datasets.

### AWS Cloud

- S3 bucket and folder organization.
- Data lake storage.
- Glue Data Catalog.
- Athena external tables.
- Serverless SQL analytics.

### GenAI and Application Development

- API integration.
- Prompt construction.
- AI-based text summarization.
- Streamlit application development.
- Interactive data visualization.

---

## 22. Final Project Summary

This project demonstrates an end-to-end insurance data engineering workflow.

Raw insurance CSV data is explored and loaded into MySQL using Python. PySpark is used to clean and transform the datasets into Silver and Gold layers. The datasets are stored in Amazon S3, registered in the AWS Glue Data Catalog, and queried using Amazon Athena.

The Streamlit frontend presents business analytics and claim details, while Ollama Cloud provides AI-generated summaries of claim notes.

The project combines **SQL, Python, PySpark, AWS, Data Warehousing, GenAI, and frontend development** into one practical cloud data engineering solution.

---

## 23. Security and Cost Precautions

- Never commit `.env` or API keys to Git.
- Never share MySQL passwords, AWS passwords, or access keys.
- Keep S3 buckets private.
- Use only the AWS permissions required for the project.
- Avoid unnecessary AWS services and scheduled jobs.
- Remember that Athena queries can incur charges based on data scanned.
- Stop or remove paid resources when they are no longer needed.
- Use synthetic data for demonstrations and testing.