import streamlit as st
import requests

# Set up the Streamlit UI
st.title("💥 Worst-Case AI Scenario Analyzer")

# User input for real-life scenario
scenario = st.text_area("Enter a real-life scenario")

if st.button("Analyze"):
    if scenario:
        # Send request to the backend API
        response = requests.post("http://127.0.0.1:8000/predict", json={"scenario": scenario})

        if response.status_code == 200:
            data = response.json()
            st.subheader("📉 Worst-Case Outcome")
            st.write(data['worst_case'])

            st.subheader("🛠️ Recommended Solution")
            st.write(data['solution'])
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    else:
        st.warning("Please enter a scenario.")