
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, URL, text
from getpass import getpass

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
RAW_FOLDER = PROJECT_FOLDER / "data" / "raw"

DATABASE = "insurance_claims_db"
USERNAME = "root"
HOST = "localhost"
PORT = 3306

# ==========================================
# 2. GET MYSQL PASSWORD SECURELY
# ==========================================

password = getpass("Enter your MySQL root password: ")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=USERNAME,
    password=password,
    host=HOST,
    port=PORT,
    database=DATABASE
)

engine = create_engine(connection_url)

# ==========================================
# 3. DEFINE CSV TO MYSQL MAPPING
# ==========================================

datasets = [
    ("policies", "policies"),
    ("beneficiaries", "beneficiaries"),
    ("claims", "claims"),
    ("claims_fraud", "claims_fraud"),
    ("claims_notes", "claims_notes")
]

# ==========================================
# 4. FIND CSV FILES
# ==========================================

def find_csv(dataset_name):

    matches = [
        path for path in RAW_FOLDER.glob("*.csv")
        if path.name.lower().startswith(dataset_name + ".")
    ]

    if len(matches) != 1:
        raise FileNotFoundError(
            f"Expected one CSV for {dataset_name}, "
            f"but found: {[p.name for p in matches]}"
        )

    return matches[0]


# ==========================================
# 5. LOAD AND VALIDATE DATA
# ==========================================

date_columns = {
    "policies": ["start_date", "end_date"],
    "beneficiaries": ["date_of_birth"],
    "claims": ["submitted_at", "created_at", "updated_at"],
    "claims_fraud": ["created_at"],
    "claims_notes": ["created_at", "updated_at"]
}

nullable_date_columns = {
    "policies": ["end_date"],
    "claims": ["updated_at"]
}

def prepare_dataframe(table_name, csv_path):

    df = pd.read_csv(csv_path)

    # Rename source column to match MySQL table
    if table_name == "policies":
        df = df.rename(columns={"type": "policy_type"})

    # Check for unexpected or missing columns
    expected_columns = {
        "policies": [
            "id", "policy_number", "policy_type",
            "start_date", "end_date"
        ],
        "beneficiaries": [
            "id", "policy_id", "name",
            "relationship", "date_of_birth"
        ],
        "claims": [
            "id", "policy_id", "status", "amount",
            "submitted_at", "created_at", "updated_at"
        ],
        "claims_fraud": [
            "id", "claim_id", "investigation_notes",
            "created_at", "fraud_type", "outcome"
        ],
        "claims_notes": [
            "id", "claim_id", "note",
            "created_at", "priority", "updated_at"
        ]
    }

    expected = expected_columns[table_name]

    if set(df.columns) != set(expected):
        raise ValueError(
            f"Column mismatch in {csv_path.name}\n"
            f"Expected: {expected}\n"
            f"Received: {df.columns.tolist()}"
        )

    df = df[expected].copy()

    # Convert dates
    for column in date_columns[table_name]:

        original = df[column]

        converted = pd.to_datetime(
            original, errors="coerce"
        )

        invalid = original.notna() & converted.isna()

        if invalid.any():
            raise ValueError(
                f"Invalid dates in {table_name}.{column}"
            )

        if column not in nullable_date_columns.get(
            table_name, []
        ) and converted.isna().any():
            raise ValueError(
                f"Missing required dates in {table_name}.{column}"
            )

        df[column] = converted.dt.date

    # Check primary key uniqueness
    if df["id"].isna().any() or df["id"].duplicated().any():
        raise ValueError(
            f"Invalid or duplicate primary keys in {table_name}"
        )

    # Check required values
    if table_name in ["beneficiaries", "claims"]:
        if df["policy_id"].isna().any():
            raise ValueError(
                f"Missing policy_id in {table_name}"
            )

    if table_name in ["claims_fraud", "claims_notes"]:
        if df["claim_id"].isna().any():
            raise ValueError(
                f"Missing claim_id in {table_name}"
            )

    return df


# ==========================================
# 6. LOAD DATA INTO MYSQL
# ==========================================

def main():

    if not RAW_FOLDER.exists():
        raise FileNotFoundError("Raw folder does not exist")

    print("\nConnecting to MySQL...")

    with engine.begin() as connection:

        # Avoid accidental duplicate imports
        for table_name, _ in datasets:

            count = connection.execute(
                text(f"SELECT COUNT(*) FROM `{table_name}`")
            ).scalar_one()

            if count > 0:
                raise RuntimeError(
                    f"{table_name} already contains {count} rows. "
                    "Import cancelled to avoid duplicates."
                )

        print("MySQL connection successful.")

        total_records = 0

        for table_name, dataset_name in datasets:

            csv_path = find_csv(dataset_name)

            print(f"\nLoading {csv_path.name}...")

            df = prepare_dataframe(table_name, csv_path)

            df.to_sql(
                name=table_name,
                con=connection,
                if_exists="append",
                index=False,
                chunksize=100,
                method="multi"
            )

            loaded_count = len(df)
            total_records += loaded_count

            print(
                f"Successfully loaded {loaded_count} "
                f"records into {table_name}"
            )

        print("\nAll datasets loaded successfully!")
        print("Total records loaded:", total_records)


if __name__ == "__main__":

    try:
        main()

    except Exception as error:
        print("\nDATA LOADING FAILED")
        print("Reason:", error)
        print("The database transaction was rolled back.")

    finally:
        engine.dispose()
