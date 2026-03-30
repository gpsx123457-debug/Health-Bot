import pandas as pd
import numpy as np
import os
import joblib
import gdown

# -------------------------------
# FILE PATHS
# -------------------------------
MODEL_PATH = "model.pkl"
FEATURES_PATH = "features.pkl"

# 🔴 PUT YOUR GOOGLE DRIVE FILE IDs HERE
MODEL_FILE_ID = "1YmORJRpUVEkmI9NIWpTzjwBkNKhNH8ar"
FEATURES_FILE_ID = "1ILfTrXLn2dVQ4gq_nMSPwI69JiQ29ZMc"


# -------------------------------
# DOWNLOAD FILE (SAFE)
# -------------------------------
def download_file(file_id, output):
    if not os.path.exists(output):
        try:
            url = f"https://drive.google.com/uc?id={file_id}"
            print(f"Downloading {output}...")
            gdown.download(url, output, quiet=False)
        except Exception as e:
            print(f"Download failed: {e}")


# -------------------------------
# LOAD MODEL + FEATURES
# -------------------------------
def load_model():
    download_file(MODEL_FILE_ID, MODEL_PATH)
    download_file(FEATURES_FILE_ID, FEATURES_PATH)

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("model.pkl missing")

    if not os.path.exists(FEATURES_PATH):
        raise FileNotFoundError("features.pkl missing")

    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)

    return model, features


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

    # Ensure all features exist
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

    # Reliability
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