# Insurance Claims Data Warehouse — Architecture

## Architecture Flow

1. Data Sources: Five insurance CSV datasets and MySQL database.
2. Python Ingestion: Loads CSV data into MySQL.
3. Bronze Layer: Stores original CSV files in Amazon S3.
4. Silver Layer: PySpark cleans data and stores transformed Parquet files in Amazon S3.
5. Gold Layer: PySpark generates claim summary, policy analysis, and fraud analysis datasets.
6. AWS Glue Data Catalog: Stores metadata and manually registered table definitions.
7. Amazon Athena: Queries Gold Parquet datasets using SQL.

## Data Flow

CSV Files + MySQL
        |
        v
Python Ingestion
        |
        v
Amazon S3 — Bronze
        |
        v
PySpark Transformation
        |
        v
Amazon S3 — Silver
        |
        v
PySpark Aggregation
        |
        v
Amazon S3 — Gold
        |
        v
AWS Glue Data Catalog
        |
        v
Amazon Athena
        |
        v
Business Analytics

## Gold Datasets

- claim_summary
- policy_analysis
- fraud_analysis

## Architecture Pattern

Medallion Architecture: Bronze → Silver → Gold