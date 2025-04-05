import pickle

# Specify the path to your label encoder file
file_path = 'models/label_encoder.pkl'

# Attempt to load the label encoder
try:
    with open(file_path, 'rb') as f:
        label_encoder = pickle.load(f)
    print("Label encoder loaded successfully!")
except Exception as e:
    print(f"Error loading label encoder: {e}")