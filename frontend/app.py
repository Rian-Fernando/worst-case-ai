import streamlit as st
import requests
import time

# Title of the app
st.title("💥 Worst-Case AI Scenario Analyzer")

# Input Section: Allowing users to describe their situation
st.subheader("Describe your real-life situation:")

scenario = st.text_area(
    "Enter your scenario here",
    placeholder="Example: I missed my final exam and now I might fail the semester.",
    height=150
)

# Button to submit the input
if st.button('Analyze Worst-Case Scenario'):
    if scenario:
        with st.spinner('Analyzing...'):
            # Send the scenario to the FastAPI backend
            try:
                response = requests.post(
                    "http://127.0.0.1:10000/predict", 
                    headers={"Content-Type": "application/json"},
                    json={"scenario": scenario}
                )
                # Check if response is successful
                if response.status_code == 200:
                    data = response.json()
                    st.success("💥 Analysis Complete!")
                    st.write(f"### Input Scenario: {data['input_scenario']}")
                    st.write(f"### Worst-Case Outcome: {data['worst_case']}")
                    st.write(f"### Solution: {data['solution']}")
                else:
                    st.error("❌ Something went wrong with the analysis.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid scenario to proceed.")

# Logging and display of previous scenarios (from the CSV file)
st.subheader("🔙 Previously Entered Scenarios:")

# Check if logged_scenarios.csv exists to avoid breaking
try:
    import pandas as pd
    df = pd.read_csv('datasets/logged_scenarios.csv')
    if not df.empty:
        st.write(df.tail(5))  # Display the latest 5 entries
except FileNotFoundError:
    st.warning("No previous scenarios logged yet.")
except Exception as e:
    st.error(f"❌ Error displaying past scenarios: {str(e)}")

# Add a footer or description about the project
st.markdown("""
    ## About this app
    This is a Worst-Case Scenario Analyzer powered by AI. It helps users by taking a real-life scenario and providing potential worst-case outcomes along with viable solutions.
    - **Backend**: Powered by FastAPI and scikit-learn.
    - **Frontend**: Built with Streamlit.
""")