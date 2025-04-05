import torch
import torch.nn as nn
import torch.optim as optim
import random

# Define a simple Transformer-based AI model
class WorstCaseAI(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(WorstCaseAI, self).__init__()
        self.embedding = nn.Embedding(input_dim, hidden_dim)
        self.lstm = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        output = self.fc(lstm_out[:, -1, :])  # Take last LSTM output
        return output

# Initialize the model
input_dim = 1000  # Vocabulary size (can be updated later)
hidden_dim = 128  # Hidden layer size
output_dim = 5    # Number of worst-case categories (adjustable)

model = WorstCaseAI(input_dim, hidden_dim, output_dim)

# Sample dummy data for testing
def generate_dummy_data(num_samples=10):
    data = []
    categories = ["Financial loss", "Legal issues", "Reputation damage", "Operational failure", "Security breach"]
    for _ in range(num_samples):
        input_text = torch.randint(0, input_dim, (10,))  # Random tokenized input
        output_label = torch.tensor(random.randint(0, output_dim - 1))  # Random category
        solution = f"Suggested solution for {categories[output_label]}."
        data.append((input_text, output_label, solution))
    return data

# Dummy training process
def train_dummy_model(model, data, epochs=5):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(epochs):
        total_loss = 0
        for input_text, output_label, _ in data:
            optimizer.zero_grad()
            prediction = model(input_text.unsqueeze(0))  # Add batch dimension
            loss = criterion(prediction, output_label.unsqueeze(0))  # Compute loss
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}")

# Generate dummy data and train the model
dummy_data = generate_dummy_data()
train_dummy_model(model, dummy_data)
