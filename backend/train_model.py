import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Dummy dataset
data = {
    "income": [25000, 40000, 15000, 50000, 30000, 20000, 45000, 35000],
    "loan_amount": [10000, 20000, 5000, 25000, 15000, 8000, 22000, 12000],
    "cibil_score": [650, 750, 600, 800, 700, 580, 770, 720],
    "default": [1, 0, 1, 0, 0, 1, 0, 0]
}

df = pd.DataFrame(data)

X = df[["income", "loan_amount", "cibil_score"]]
y = df["default"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, "loan_model.pkl")

print("Model trained and saved!")