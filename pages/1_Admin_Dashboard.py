import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")
st.title("Admin Analytics Dashboard")

# Function to load events from jsonl
@st.cache_data(ttl=60)
def load_events():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    events_path = os.path.join(base_dir, "data", "analytics", "events.jsonl")
    
    if not os.path.exists(events_path):
        return pd.DataFrame()
        
    events = []
    with open(events_path, "r") as f:
        for line in f:
            if line.strip():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    
    if not events:
        return pd.DataFrame()
        
    df = pd.DataFrame(events)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

df = load_events()

if df.empty:
    st.info("No analytics data available yet. Start querying the assistant to generate data.")
    st.stop()

# 1. Total events metric
st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)

total_queries = len(df[df["event_type"] == "query_received"])
total_answers = len(df[df["event_type"] == "answer_served"])
total_pii_blocks = len(df[df["event_type"] == "pii_blocked"])
total_refusals = len(df[df["event_type"] == "refusal_served"])

col1.metric("Total Queries", total_queries)
col2.metric("Answers Served", total_answers)
col3.metric("PII Blocks", total_pii_blocks)
col4.metric("Refusals", total_refusals)

st.divider()

# 2. Intent Breakdown
st.subheader("Query Intents")
if "event_type" in df.columns and "intent" in df.columns:
    intent_df = df[df["event_type"] == "query_received"].dropna(subset=["intent"])
    if not intent_df.empty:
        intent_counts = intent_df["intent"].value_counts()
        st.bar_chart(intent_counts)

# 3. Refusals Breakdown
st.subheader("Refusal Reasons")
if "event_type" in df.columns and "refusal_type" in df.columns:
    refusal_df = df[df["event_type"] == "refusal_served"].dropna(subset=["refusal_type"])
    if not refusal_df.empty:
        refusal_counts = refusal_df["refusal_type"].value_counts()
        st.bar_chart(refusal_counts)

# 4. Recent Events
st.subheader("Recent Event Logs")
st.dataframe(df.sort_values(by="timestamp", ascending=False).head(50), use_container_width=True)
