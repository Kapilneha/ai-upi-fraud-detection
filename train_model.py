import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Sample transaction data
data = {
    "amount": [100, 200, 500, 1000, 7000, 9000, 12000, 300],
    "is_foreign": [0, 0, 0, 0, 1, 1, 1, 1],
    "fraud": [0, 0, 0, 0, 1, 1, 1, 0]
}

# Convert into DataFrame
df = pd.DataFrame(data)

# Features
X = df[["amount", "is_foreign"]]

# Target
y = df["fraud"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2
)

# Create model
model = RandomForestClassifier()

# Train model
model.fit(X_train, y_train)

# Save model
with open("fraud_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model trained successfully!")