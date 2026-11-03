
import pandas as pd
from pathlib import Path

# Locate project folders
PROJECT_FOLDER = Path(__file__).resolve().parents[1]
RAW_FOLDER = PROJECT_FOLDER / "data" / "raw"

print("Project:", PROJECT_FOLDER)
print("Raw data:", RAW_FOLDER)

# Check raw folder
if not RAW_FOLDER.exists():
    raise FileNotFoundError("Raw folder not found")

csv_files = list(RAW_FOLDER.glob("*.csv"))

print("Total CSV files:", len(csv_files))

# Explore each file
for file_path in csv_files:

    print("\n" + "=" * 60)
    print("FILE:", file_path.name)
    print("=" * 60)

    df = pd.read_csv(file_path)

    print("\nRows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nFirst five records:")
    print(df.head().to_string(index=False))
