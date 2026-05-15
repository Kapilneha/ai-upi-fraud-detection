import streamlit as st
import requests
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="UPI Fraud Detection",
    page_icon="🚨",
    layout="wide"
)

st.markdown(
    """
    Real-time fraud detection dashboard using
    Machine Learning, FastAPI and Streamlit.
    """
)

st.write("Check whether a transaction is fraudulent.")

# User Inputs
amount = st.number_input(
    "Transaction Amount",
    min_value=0.0
)

is_foreign = st.selectbox(
    "Foreign Transaction?",
    [0, 1]
)

# Prediction Button
if st.button("Check Fraud"):

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        params={
            "amount": amount,
            "is_foreign": is_foreign
        }
    )

    result = response.json()

    st.subheader("Prediction Result")

    if result["prediction"] == "Fraud":
        st.error("⚠️ Fraudulent Transaction Detected")
    else:
        st.success("✅ Safe Transaction")

    st.write(
    "Reason:",
    result["reason"]
)

# Transaction History
st.subheader("Transaction History")

history = requests.get(
    "http://127.0.0.1:8000/transactions"
)

history_data = history.json()

# Convert single object into list if needed
if isinstance(history_data, dict):
    history_data = [history_data]

df = pd.DataFrame(history_data)
st.dataframe(df)

# Metrics Section

st.subheader("System Metrics")

if not df.empty:

    total_transactions = len(df)

    fraud_transactions = (
        df["prediction"] == "Fraud"
    ).sum()

    safe_transactions = (
        df["prediction"] == "Safe"
    ).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Transactions",
        total_transactions
    )

    col2.metric(
        "Fraud Transactions",
        fraud_transactions
    )

    col3.metric(
        "Safe Transactions",
        safe_transactions
    )

# Fraud Analytics

st.subheader("Fraud Analytics")

if not df.empty:

    fraud_count = (
        df["prediction"] == "Fraud"
    ).sum()

    safe_count = (
        df["prediction"] == "Safe"
    ).sum()

    chart_data = {
        "Category": ["Fraud", "Safe"],
        "Count": [fraud_count, safe_count]
    }

    chart_df = pd.DataFrame(chart_data)

    fig = px.pie(
        chart_df,
        values="Count",
        names="Category",
        title="Fraud vs Safe Transactions"
    )

    st.plotly_chart(fig)

st.markdown("---")

st.caption(
    "Built using FastAPI, Streamlit, Scikit-learn and SQLite"
)