
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from ollama import Client

# Project paths
PROJECT_DIR = Path(__file__).resolve().parents[1]
NOTES_FILE = PROJECT_DIR / "data" / "raw" / "claims_notes.csv.csv"

# Load API credentials
load_dotenv(PROJECT_DIR / ".env")

api_key = os.getenv("OLLAMA_API_KEY")
model = os.getenv("OLLAMA_MODEL")

if not api_key or not model:
    raise ValueError("Ollama credentials missing in .env")

# Connect to Ollama Cloud
client = Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {api_key}"}
)

# Read actual claim notes
notes_df = pd.read_csv(NOTES_FILE)

print("\nAvailable Claim IDs:")
print(sorted(notes_df["claim_id"].unique()))

# Ask user for claim ID
claim_id = int(input("\nEnter Claim ID: "))

# Filter notes for selected claim
selected_notes = notes_df[
    notes_df["claim_id"] == claim_id
]

if selected_notes.empty:
    print("No notes found for this claim ID.")
    raise SystemExit

# Combine all notes
claim_notes = "\n".join(
    selected_notes["note"].dropna().astype(str).tolist()
)

print("\nSending claim notes to AI...")

prompt = f"""
You are an insurance claims analysis assistant.

Analyze the following insurance claim notes.

Provide:
1. Short claim summary
2. Important risk indicators mentioned in the notes
3. Missing or unclear information
4. Suggested next action for the reviewer

Important:
- Do not invent facts.
- Do not treat an indicator as proof of fraud.
- Do not make a final approval or rejection decision.
- Clearly state when information is insufficient.

Claim ID: {claim_id}

Claim Notes:
{claim_notes}
"""

response = client.chat(
    model=model,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("\n========== AI CLAIM ANALYSIS ==========")
print(response.message.content)
print("\n=======================================")
