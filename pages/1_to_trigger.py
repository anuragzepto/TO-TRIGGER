import streamlit as st
import requests
import json

# --- Load secrets ---
DATABRICKS_API_URL = st.secrets["DATABRICKS_API_URL"]
DATABRICKS_TOKEN = st.secrets["DATABRICKS_TOKEN"]
JOB_ID = st.secrets["JOB_ID"]

st.set_page_config(page_title="Trigger Job", page_icon="🚀")

# --- Auth check ---
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("You must login from the home page to access this page.")
    st.stop()

# --- UI ---
st.title("Trigger Databricks Job")

mh_code = st.text_input("Enter MH Code(s)", value="KOL004M,SON004M")

if st.button("Trigger Job"):
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "job_id": JOB_ID,
        "notebook_params": {
            "mh_code": mh_code
        }
    }

    response = requests.post(DATABRICKS_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        run_id = response.json().get("run_id")
        st.success(f"Job triggered successfully! Run ID: {run_id}")
    else:
        st.error(f"Failed to trigger job. Status: {response.status_code}")
        st.code(response.text)
