from fastapi import FastAPI
import pickle
import numpy as np

from database import SessionLocal, Transaction

app = FastAPI()

# Load ML model
model = pickle.load(open("fraud_model.pkl", "rb"))

@app.get("/")
def home():
    return {"message": "Fraud Detection API Running"}

@app.post("/predict")
def predict(amount: float, is_foreign: int):

    prediction = model.predict(
        np.array([[amount, is_foreign]])
    )

    result = "Fraud" if prediction[0] == 1 else "Safe"

    db = SessionLocal()

    transaction = Transaction(
        amount=amount,
        is_foreign=is_foreign,
        prediction=result
    )

    db.add(transaction)
    db.commit()
    db.close()

    reason = ""

    if amount > 5000 and is_foreign == 1:
        reason = (
            "High amount and foreign transaction detected"
        )

    elif amount > 5000:
        reason = (
            "Unusually high transaction amount"
        )

    elif is_foreign == 1:
        reason = (
            "Foreign transaction detected"
        )

    else:
        reason = (
            "Transaction appears normal"
        )

    return {
        "prediction": result,
        "reason": reason
    }
@app.get("/transactions")
def get_transactions():

    db = SessionLocal()

    transactions = db.query(Transaction).all()

    db.close()

    return transactions