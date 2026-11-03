
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

# ----------------------------------------
# 1. Project paths
# ----------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------
# 2. Start Spark
# ----------------------------------------

spark = (
    SparkSession.builder
    .appName("InsuranceClaimsCleaning")
    .master("local[*]")
    .config("spark.hadoop.fs.permissions.umask-mode", "000")
    .config("spark.hadoop.fs.file.impl", 
            "org.apache.hadoop.fs.RawLocalFileSystem")
    .config("spark.hadoop.fs.permissions.enabled", "false")
    .config("spark.local.dir", str(PROJECT_DIR / "temp" / "spark"))
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# ----------------------------------------
# 3. Define source files and date columns
# ----------------------------------------

datasets = {
    "policies": {
        "file": "policies.csv.csv",
        "dates": ["start_date", "end_date"]
    },
    "beneficiaries": {
        "file": "beneficiaries.csv.csv",
        "dates": ["date_of_birth"]
    },
    "claims": {
        "file": "claims.csv.csv",
        "dates": ["submitted_at", "created_at", "updated_at"]
    },
    "claims_fraud": {
        "file": "claims_fraud.csv.csv",
        "dates": ["created_at"]
    },
    "claims_notes": {
        "file": "claims_notes.csv.csv",
        "dates": ["created_at", "updated_at"]
    }
}

# ----------------------------------------
# 4. Read, clean and transform each dataset
# ----------------------------------------

for table_name, config in datasets.items():

    print(f"\n========== Processing {table_name} ==========")

    input_path = RAW_DIR / config["file"]

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(input_path))
    )

    original_count = df.count()

    # Trim whitespace and convert empty strings to NULL
    for field in df.schema.fields:
        if isinstance(field.dataType, StringType):
            column_name = field.name

            df = df.withColumn(
                column_name,
                F.when(
                    F.length(F.trim(F.col(column_name))) == 0,
                    F.lit(None)
                ).otherwise(F.trim(F.col(column_name)))
            )

    # Standardize date columns
    for date_column in config["dates"]:
        df = df.withColumn(
            date_column,
            F.to_date(F.col(date_column).cast("string"), "yyyy-MM-dd")
        )

    # Standardize claim amount
    if table_name == "claims":
        df = df.withColumn(
            "amount",
            F.col("amount").cast("decimal(12,2)")
        )

        # Preserve missing amounts and identify them
        df = df.withColumn(
            "is_amount_missing",
            F.col("amount").isNull()
        )

    # Rename source column for consistency
    if table_name == "policies":
        df = df.withColumnRenamed("type", "policy_type")

    # Check duplicate primary keys
    duplicate_count = (
        df.groupBy("id")
        .count()
        .filter(F.col("count") > 1)
        .count()
    )

    # Save cleaned dataset as Parquet
    output_path = PROCESSED_DIR / table_name

    (
        df.write
        .mode("overwrite")
        .parquet(str(output_path))
    )

    print("Original rows:", original_count)
    print("Rows after cleaning:", df.count())
    print("Duplicate primary keys:", duplicate_count)
    print("Output:", output_path)

    print("Cleaned schema:")
    df.printSchema()

    print("Sample records:")
    df.show(5, truncate=False)

spark.stop()

print("\nAll five datasets processed successfully.")
