import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Disable tokenizer parallelism

import streamlit as st
import pandas as pd
from classify import classify
import asyncio

# Ensure an asyncio event loop exists
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

st.title("Log Classification App")
st.markdown("Upload a CSV file with columns `source` and `log_message` to perform log classification, or click the button below to use a default test CSV.")

# File uploader for user CSV
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

# Button to use the default test CSV
use_test_csv = st.button("Use Test CSV")

# Function to process a DataFrame
def process_dataframe(df):
    st.subheader("Input Data Sample")
    st.dataframe(df.head())
    
    # Validate required columns
    if "source" not in df.columns or "log_message" not in df.columns:
        st.error("CSV must contain 'source' and 'log_message' columns.")
        return None

    # Show a spinner while processing classification
    with st.spinner("Classifying logs..."):
        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))
    
    st.subheader("Output Data Sample")
    st.dataframe(df.head())
    
    # Prepare CSV for download
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Output CSV",
        data=csv_data,
        file_name="output.csv",
        mime="text/csv"
    )
    return df

# Process the uploaded file if provided
if uploaded_file is not None:
    try:
        df_input = pd.read_csv(uploaded_file)
        process_dataframe(df_input)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# If no file is uploaded and the user clicks the test CSV button
elif use_test_csv:
    try:
        df_input = pd.read_csv("resources/test.csv")
        process_dataframe(df_input)
    except Exception as e:
        st.error(f"An error occurred while loading the test CSV: {e}")