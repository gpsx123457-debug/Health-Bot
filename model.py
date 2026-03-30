import pandas as pd
import numpy as np
import joblib

# -------------------------------
# LOAD MODEL + FEATURES (LOCAL)
# -------------------------------
def load_model():
    try:
        model = joblib.load("model.pkl")
        features = joblib.load("features.pkl")
        return model, features
    except Exception as e:
        raise RuntimeError(f"Model loading failed: {e}")


# -------------------------------
# PREPROCESS INPUT
# -------------------------------
def preprocess_input(user_input):
    processed = user_input.copy()

    # Duration bucket
    days = processed.get("Duration", 1)

    if days <= 2:
        processed["Duration"] = 0
    elif days <= 5:
        processed["Duration"] = 1
    else:
        processed["Duration"] = 2

    return processed


# -------------------------------
# PREDICT FUNCTION
# -------------------------------
def predict(user_input_dict):
    model, features = load_model()

    user_input = preprocess_input(user_input_dict)

    # Ensure feature alignment
    input_data = [user_input.get(f, 0) for f in features]
    input_df = pd.DataFrame([input_data], columns=features)

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    confidence = float(np.max(probabilities) * 100)

    # Top 3 predictions
    top3_idx = np.argsort(probabilities)[-3:][::-1]
    top3 = [
        (model.classes_[i], round(probabilities[i] * 100, 2))
        for i in top3_idx
    ]

    reliability = (
        "High" if confidence >= 80 else
        "Moderate" if confidence >= 60 else
        "Low"
    )

    return {
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "top3": top3,
        "reliability": reliability
    }