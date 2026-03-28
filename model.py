import pandas as pd
import numpy as np
import pickle
import os
import requests

# -------------------------------
# CONFIG
# -------------------------------
MODEL_PATH = "model.pkl"
FEATURES_PATH = "features.pkl"

# 🔴 PASTE YOUR GOOGLE DRIVE DIRECT LINK HERE
MODEL_URL = "https://drive.google.com/file/d/1YmORJRpUVEkmI9NIWpTzjwBkNKhNH8ar/view?usp=sharing"


# -------------------------------
# DOWNLOAD MODEL (IF NOT PRESENT)
# -------------------------------
def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model...")

        try:
            r = requests.get(MODEL_URL)
            r.raise_for_status()

            with open(MODEL_PATH, "wb") as f:
                f.write(r.content)

            print("Model downloaded successfully.")

        except Exception as e:
            raise RuntimeError(f"Failed to download model: {e}")


# -------------------------------
# LOAD MODEL
# -------------------------------
def load_model():
    # Download model if missing
    download_model()

    # Check features file
    if not os.path.exists(FEATURES_PATH):
        raise FileNotFoundError("features.pkl not found. Upload it to GitHub.")

    # Load model
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    # Load features
    with open(FEATURES_PATH, "rb") as f:
        features = pickle.load(f)

    return model, features


# -------------------------------
# HELPER: NORMALIZE INPUT
# -------------------------------
def preprocess_input(user_input):
    processed = user_input.copy()

    # Duration normalization
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

    # Preprocess input
    user_input = preprocess_input(user_input_dict)

    # Align features
    input_data = [user_input.get(f, 0) for f in features]
    input_df = pd.DataFrame([input_data], columns=features)

    # Prediction
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    # Confidence
    confidence = float(np.max(probabilities) * 100)

    # Top 3 predictions
    top3_idx = np.argsort(probabilities)[-3:][::-1]
    top3 = [
        (model.classes_[i], round(probabilities[i] * 100, 2))
        for i in top3_idx
    ]

    # Reliability
    if confidence >= 80:
        reliability = "High"
    elif confidence >= 60:
        reliability = "Moderate"
    else:
        reliability = "Low"

    return {
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "top3": top3,
        "reliability": reliability
    }