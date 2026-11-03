
import os
from dotenv import load_dotenv
from ollama import Client

load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")
model = os.getenv("OLLAMA_MODEL")

if not api_key or not model:
    raise ValueError("OLLAMA_API_KEY or OLLAMA_MODEL missing in .env")

# Connect to Ollama Cloud
client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + api_key}
)

claim_notes = """
The customer submitted a claim for vehicle damage
after a road accident.

The customer reported damage to the front bumper.
The repair estimate is 45000.
Accident photographs are available.

The insurance team needs to verify the repair estimate
and supporting documents before approval.
"""

prompt = f"""
You are an insurance claims analysis assistant.

Analyze these claim notes and provide:

1. Short claim summary
2. Important risk indicators
3. Missing information
4. Suggested next action

Do not make a final approval or rejection decision.
Do not invent facts.

Claim notes:
{claim_notes}
"""

response = client.chat(
    model=model,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print("\n===== AI CLAIM ANALYSIS =====\n")
print(response.message.content)
