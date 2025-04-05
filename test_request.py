import requests

url = "https://worst-case-ai.onrender.com/predict"
headers = {
    "Content-Type": "application/json"
}
data = {
    "CPU Usage (%)": 75.0,
    "Memory Usage (%)": 65.0,
    "Network Traffic (B/s)": 5000.0
}

response = requests.post(url, json=data, headers=headers)

print("Status code:", response.status_code)
print("Response:", response.json())