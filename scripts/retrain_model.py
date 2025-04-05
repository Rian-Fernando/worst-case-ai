import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import joblib

# Path to the new logged scenarios CSV
CSV_PATH = 'datasets/logged_scenarios.csv'

# Function to retrain the model
def retrain_model():
    print("📚 Retraining model on new scenarios...")

    # Read the new CSV data
    df = pd.read_csv(CSV_PATH)

    # Prepare the features and labels
    X = df['scenario']
    y = df['worst_case']

    # Convert text data to numerical vectors
    vectorizer = CountVectorizer(stop_words='english')
    X_vect = vectorizer.fit_transform(X)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.2, random_state=42)

    # Create and train the Logistic Regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Save the retrained model
    joblib.dump(model, 'models/failure_model.pkl')
    joblib.dump(vectorizer, 'models/vectorizer.pkl')  # Save the vectorizer as well for later use

    print("✅ Model retrained and saved.")