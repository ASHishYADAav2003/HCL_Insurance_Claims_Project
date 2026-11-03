
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from ollama import Client

# ---------------- PROJECT CONFIGURATION ----------------

PROJECT_DIR = Path(__file__).resolve().parent
GOLD_DIR = PROJECT_DIR / "data" / "gold"
NOTES_FILE = PROJECT_DIR / "data" / "raw" / "claims_notes.csv.csv"

load_dotenv(PROJECT_DIR / ".env")

st.set_page_config(
    page_title="Insurance Claims Assistant",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD GOLD DATA ----------------

@st.cache_data
def load_gold_data():
    claim_summary = pd.read_parquet(
        GOLD_DIR / "claim_summary"
    )

    policy_analysis = pd.read_parquet(
        GOLD_DIR / "policy_analysis"
    )

    fraud_analysis = pd.read_parquet(
        GOLD_DIR / "fraud_analysis"
    )

    notes = pd.read_csv(NOTES_FILE)

    return claim_summary, policy_analysis, fraud_analysis, notes


try:
    claim_summary, policy_analysis, fraud_analysis, notes = (
        load_gold_data()
    )
except Exception as error:
    st.error(f"Could not load project data: {error}")
    st.stop()


# ---------------- SIDEBAR ----------------

st.sidebar.title("Insurance Claims")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Claim Details", "AI Claims Assistant"]
)


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.title("📊 Insurance Claims Dashboard")
    st.caption("Insurance Claims Data Warehouse — HCLTech Project")

    total_claims = int(claim_summary["total_claims"].sum())

    approved = int(
        claim_summary.loc[
            claim_summary["status"] == "approved",
            "total_claims"
        ].sum()
    )

    denied = int(
        claim_summary.loc[
            claim_summary["status"] == "denied",
            "total_claims"
        ].sum()
    )

    missing = int(
        claim_summary["missing_amount_count"].sum()
    )

    approval_rate = (
        approved / total_claims * 100
        if total_claims else 0
    )

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Claims", total_claims)
    col2.metric("Approved Claims", approved)
    col3.metric("Denied Claims", denied)
    col4.metric("Approval Rate", f"{approval_rate:.2f}%")

    st.divider()

    # Claim status chart
    st.subheader("Claims by Status")

    status_chart = px.bar(
        claim_summary,
        x="status",
        y="total_claims",
        color="status",
        title="Number of Claims by Status"
    )

    st.plotly_chart(status_chart, use_container_width=True)

    # Policy analysis
    st.subheader("Policy-wise Claim Analysis")

    policy_chart = px.bar(
        policy_analysis,
        x="policy_type",
        y="total_claims",
        color="policy_type",
        title="Claims by Policy Type"
    )

    st.plotly_chart(policy_chart, use_container_width=True)

    # Fraud analysis
    st.subheader("Fraud Investigation Analysis")

    fraud_chart = px.bar(
        fraud_analysis,
        x="fraud_type",
        y="total_investigations",
        color="outcome",
        barmode="group",
        title="Fraud Investigations by Type and Outcome"
    )

    st.plotly_chart(fraud_chart, use_container_width=True)

    st.metric("Claims with Missing Amount", missing)

    st.subheader("Claim Summary Data")
    st.dataframe(claim_summary, use_container_width=True)



# ---------------- CLAIM DETAILS ----------------

elif page == "Claim Details":

    st.title("📋 Claim Details Explorer")

    claim_ids = sorted(
        notes["claim_id"].dropna().unique().tolist()
    )

    selected_claim = st.selectbox(
        "Select Claim ID",
        claim_ids
    )

    selected_notes = notes[
        notes["claim_id"] == selected_claim
    ]

    st.subheader(f"Claim ID: {selected_claim}")

    st.metric("Total Notes", len(selected_notes))

    st.dataframe(
        selected_notes,
        use_container_width=True
    )

    # Download selected claim notes
    csv_data = selected_notes.to_csv(index=False)

    st.download_button(
        label="Download Claim Notes",
        data=csv_data,
        file_name=f"claim_{selected_claim}_notes.csv",
        mime="text/csv"
    )
# ---------------- AI CLAIMS ASSISTANT ----------------

elif page == "AI Claims Assistant":

    st.title("🤖 AI Insurance Claims Assistant")

    st.write(
        "Select a claim ID to summarize its notes "
        "and identify information requiring further review."
    )

    claim_ids = sorted(notes["claim_id"].dropna().unique().tolist())

    selected_claim = st.selectbox(
        "Select Claim ID",
        claim_ids
    )

    selected_notes = notes[
        notes["claim_id"] == selected_claim
    ]

    if st.button("Generate AI Analysis", type="primary"):

        api_key = os.getenv("OLLAMA_API_KEY")
        model = os.getenv("OLLAMA_MODEL")

        if not api_key or not model:
            st.error("Ollama credentials are missing in .env.")
            st.stop()

        claim_text = "\n".join(
            selected_notes["note"].dropna().astype(str).tolist()
        )

        prompt = f"""
        You are an insurance claims analysis assistant.

        Analyze these claim notes.

        Provide:
        1. Short claim summary
        2. Important risk indicators mentioned
        3. Missing or unclear information
        4. Suggested next action for the reviewer

        Do not invent facts.
        Do not treat a risk indicator as proof of fraud.
        Do not make a final approval or rejection decision.
        Clearly mention when information is insufficient.

        Claim ID: {selected_claim}

        Claim Notes:
        {claim_text}
        """

        try:
            client = Client(
                host="https://ollama.com",
                headers={
                    "Authorization": f"Bearer {api_key}"
                }
            )

            with st.spinner("AI is analyzing the claim notes..."):

                response = client.chat(
                    model=model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

            st.subheader("AI Analysis Result")
            st.markdown(response.message.content)

        except Exception as error:
            st.error(f"AI request failed: {error}")

    st.caption(
        "AI output is advisory only. A human reviewer must verify "
        "all information before making an insurance decision."
    )
