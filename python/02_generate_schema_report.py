
import pandas as pd
from pathlib import Path

# Locate project folders
PROJECT_FOLDER = Path(__file__).resolve().parents[1]
RAW_FOLDER = PROJECT_FOLDER / "data" / "raw"
REPORT_FOLDER = PROJECT_FOLDER / "reports"

REPORT_FOLDER.mkdir(exist_ok=True)

report = []

report.append("# Insurance Claims - Dataset Schema Report\n")

csv_files = sorted(RAW_FOLDER.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV files found in data/raw")

for file_path in csv_files:

    df = pd.read_csv(file_path)

    report.append(f"\n## Dataset: {file_path.name}\n")

    report.append(f"- Rows: {df.shape[0]}")
    report.append(f"- Columns: {df.shape[1]}")
    report.append(f"- Duplicate rows: {df.duplicated().sum()}")

    report.append("\n### Column details\n")
    report.append("| Column | Pandas Type | Missing Values |")
    report.append("|---|---|---:|")

    for column in df.columns:
        dtype = str(df[column].dtype)
        missing = int(df[column].isna().sum())

        report.append(
            f"| {column} | {dtype} | {missing} |"
        )

    report.append("\n### Sample records\n")
    report.append("```text")
    report.append(df.head(5).to_string(index=False))
    report.append("```")

# Save report
output_file = REPORT_FOLDER / "schema_report.md"

output_file.write_text(
    "\n".join(report),
    encoding="utf-8"
)

print("Schema report generated successfully!")
print("Saved at:", output_file)
