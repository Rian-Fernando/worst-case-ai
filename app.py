import streamlit as st
import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model import model, generate_dummy_data

# Set up Streamlit app
st.title("Worst-Case Scenario AI 🚨")

st.write("This AI predicts worst-case outcomes based on failure scenarios.")

# User input
user_input = st.text_input("Enter a failure scenario:", "")

# Generate dummy failure cases (temporary until real data is added)
dummy_data = generate_dummy_data(50)

# Convert to DataFrame for visualization
df = pd.DataFrame(dummy_data, columns=["Input", "Category", "Solution"])

# Predict outcome
if user_input:
    input_tensor = torch.randint(0, 1000, (10,))  # Simulate tokenization
    prediction = model(input_tensor.unsqueeze(0))
    predicted_label = torch.argmax(prediction).item()
    
    worst_cases = ["Financial loss", "Legal issues", "Reputation damage", "Operational failure", "Security breach"]
    predicted_outcome = worst_cases[predicted_label]
    
    st.subheader("🔮 Predicted Worst-Case Outcome:")
    st.write(f"**{predicted_outcome}**")

    # Suggested solution
    st.subheader("💡 Suggested Solution:")
    st.write(f"Recommended action: Mitigate {predicted_outcome} risks with proper planning.")

# Data Visualization
st.subheader("📊 Worst-Case Scenario Trends")
fig, ax = plt.subplots(figsize=(8, 4))
sns.countplot(y=df[1].apply(lambda x: ["Financial loss", "Legal issues", "Reputation damage", "Operational failure", "Security breach"][x]), ax=ax)
st.pyplot(fig)
