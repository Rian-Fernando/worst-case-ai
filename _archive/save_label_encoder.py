import pickle
from sklearn.preprocessing import LabelEncoder

# Sample data for encoding, replace with your own dataset labels
labels = ['label1', 'label2', 'label3', 'label2', 'label1']  # Replace with actual labels in your dataset

# Initialize the label encoder
label_encoder = LabelEncoder()

# Fit the encoder to your labels
label_encoder.fit(labels)

# Save the trained label encoder to a file
with open('models/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

print("Label encoder saved successfully!")