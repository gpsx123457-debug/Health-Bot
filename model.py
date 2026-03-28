import pandas as pd
import numpy as np
import pickle
import os
import gdown

MODEL_PATH = "model.pkl"
FEATURES_PATH = "features.pkl"

# 🔴 MUST BE FILE ID ONLY
MODEL_FILE_ID = "1YmORJRpUVEkmI9NIWpTzjwBkNKhNH8ar"


# -------------------------------
# DOWNLOAD MODEL PROPERLY
# -------------------------------
def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model via gdown...")

        url = f"https://drive.google.com/uc?id={MODEL_FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)


# -------------------------------
# LOAD MODEL
# -------------------------------
def load_model():
    download_model()

    if not os.path.exists(FEATURES_PATH):
        raise FileNotFoundError("features.pkl missing")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(FEATURES_PATH, "rb") as f:
        features = pickle.load(f)

    return model, features


# -------------------------------
# PREPROCESS
# -------------------------------
def preprocess_input(user_input):
    processed = user_input.copy()

    days = processed.get("Duration", 1)

    if days <= 2:
        processed["Duration"] = 0
    elif days <= 5:
        processed["Duration"] = 1
    else:
        processed["Duration"] = 2

    return processed


# -------------------------------
# PREDICT
# -------------------------------
def predict(user_input_dict):
    model, features = load_model()

    user_input = preprocess_input(user_input_dict)

    input_data = [user_input.get(f, 0) for f in features]
    input_df = pd.DataFrame([input_data], columns=features)

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    confidence = float(np.max(probabilities) * 100)

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