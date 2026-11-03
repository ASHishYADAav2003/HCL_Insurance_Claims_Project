
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Project directories
PROJECT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
GOLD_DIR = PROJECT_DIR / "data" / "gold"

GOLD_DIR.mkdir(parents=True, exist_ok=True)

# Start Spark
spark = (
    SparkSession.builder
    .appName("InsuranceClaimsGoldLayer")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# Read Silver datasets
claims = spark.read.parquet(str(PROCESSED_DIR / "claims"))
policies = spark.read.parquet(str(PROCESSED_DIR / "policies"))
fraud = spark.read.parquet(str(PROCESSED_DIR / "claims_fraud"))

# ----------------------------------
# 1. Claim summary by status
# ----------------------------------

claim_summary = (
    claims.groupBy("status")
    .agg(
        F.count("*").alias("total_claims"),
        F.sum("amount").alias("total_claim_amount"),
        F.round(F.avg("amount"), 2).alias("average_claim_amount"),
        F.sum(
            F.when(F.col("amount").isNull(), 1).otherwise(0)
        ).alias("missing_amount_count")
    )
)

claim_summary.write.mode("overwrite").parquet(
    str(GOLD_DIR / "claim_summary")
)

print("\n========== CLAIM SUMMARY ==========")
claim_summary.show(truncate=False)

# ----------------------------------
# 2. Policy type analysis
# ----------------------------------

policy_analysis = (
    policies.join(claims, "id", "inner")
    if False else
    policies.join(
        claims,
        policies.id == claims.policy_id,
        "left"
    )
)

policy_analysis = (
    policy_analysis.groupBy("policy_type")
    .agg(
        F.count(claims.id).alias("total_claims"),
        F.sum("amount").alias("total_claim_amount"),
        F.round(F.avg("amount"), 2).alias("average_claim_amount")
    )
)

policy_analysis.write.mode("overwrite").parquet(
    str(GOLD_DIR / "policy_analysis")
)

print("\n========== POLICY ANALYSIS ==========")
policy_analysis.show(truncate=False)

# ----------------------------------
# 3. Fraud analysis
# ----------------------------------

fraud_analysis = (
    fraud.groupBy("fraud_type", "outcome")
    .agg(
        F.count("*").alias("total_investigations")
    )
)

fraud_analysis.write.mode("overwrite").parquet(
    str(GOLD_DIR / "fraud_analysis")
)

print("\n========== FRAUD ANALYSIS ==========")
fraud_analysis.show(truncate=False)

print("\nAll Gold datasets created successfully!")

spark.stop()
