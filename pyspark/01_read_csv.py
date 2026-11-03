
from pathlib import Path
from pyspark.sql import SparkSession

# Find the project directory
PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"

# Start Spark
spark = (
    SparkSession.builder
    .appName("InsuranceClaimsDataWarehouse")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# Read all five CSV files
files = [
    "policies.csv.csv",
    "beneficiaries.csv.csv",
    "claims.csv.csv",
    "claims_fraud.csv.csv",
    "claims_notes.csv.csv"
]

for filename in files:
    file_path = RAW_DATA_DIR / filename

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(file_path))
    )

    print(f"\n========== {filename} ==========")
    print("Total rows:", df.count())
    print("Columns:", df.columns)

    df.show(5, truncate=False)

spark.stop()
