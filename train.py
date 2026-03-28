import pandas as pd
import random
import pickle
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# -----------------------------
# SYMPTOMS
# -----------------------------
symptoms = [
    "Fever","Cough","Headache","Fatigue","Nausea","Vomiting","Diarrhea",
    "BodyPain","SoreThroat","RunnyNose","ChestPain","Breathlessness",
    "Acidity","AbdominalPain","Dizziness","Allergy","Rash","Chills",
    "Sweating","BurnInjury","Bleeding","Swelling"
]

columns = symptoms + ["Duration", "AgeGroup", "Condition", "Disease"]


# -----------------------------
# DISEASE DEFINITIONS (15)
# -----------------------------
diseases = {
    "Flu": ["Fever","Cough","Headache","Fatigue","Chills","Sweating","BodyPain"],
    "Common Cold": ["Cough","SoreThroat","RunnyNose"],
    "Typhoid": ["Fever","Fatigue","AbdominalPain","Headache"],
    "Allergy": ["Allergy","Rash","RunnyNose"],
    "Burns Mild": ["BurnInjury"],
    "Burns Severe": ["BurnInjury","Bleeding"],
    "Food Poisoning": ["Nausea","Vomiting","Diarrhea","AbdominalPain"],
    "Migraine": ["Headache","Dizziness"],
    "Gastritis": ["Acidity","AbdominalPain","Nausea"],
    "Asthma": ["Cough","Breathlessness","ChestPain"],
    "Dengue": ["Fever","BodyPain","Rash","Chills","Headache"],
    "Cuts Bruises": ["Bleeding","Swelling"],
    "Pneumonia": ["Fever","Cough","ChestPain","Breathlessness"],
    "Viral Infection": ["Fever","Fatigue","Headache","BodyPain"],
    "Skin Infection": ["Rash","Swelling","Allergy"]
}


# -----------------------------
# DATASET GENERATION (STABLE)
# -----------------------------
def generate_dataset(samples_per_disease=800):
    rows = []

    for disease, main_symptoms in diseases.items():
        for _ in range(samples_per_disease):
            row = []

            for sym in symptoms:
                if sym in main_symptoms:
                    val = 1 if random.random() < 0.9 else 0
                else:
                    val = 1 if random.random() < 0.05 else 0
                row.append(val)

            # Duration (0,1,2)
            if disease in ["Flu","Common Cold","Food Poisoning"]:
                duration = random.choices([0,1,2], weights=[0.6,0.3,0.1])[0]
            elif disease in ["Typhoid","Dengue","Pneumonia"]:
                duration = random.choices([0,1,2], weights=[0.1,0.4,0.5])[0]
            else:
                duration = random.randint(0,2)

            # AgeGroup (0,1,2)
            if disease in ["Flu","Common Cold","Allergy"]:
                age = random.choices([0,1,2], weights=[0.3,0.6,0.1])[0]
            elif disease in ["Pneumonia","Typhoid"]:
                age = random.choices([0,1,2], weights=[0.1,0.5,0.4])[0]
            else:
                age = random.randint(0,2)

            # Condition (severity)
            if disease in ["Burns Severe","Dengue","Pneumonia"]:
                condition = random.choices([0,1,2], weights=[0.1,0.3,0.6])[0]
            else:
                condition = random.choices([0,1,2], weights=[0.5,0.3,0.2])[0]

            row += [duration, age, condition, disease]
            rows.append(row)

    df = pd.DataFrame(rows, columns=columns)
    df = df.sample(frac=1).reset_index(drop=True)

    df.to_csv("dataset.csv", index=False)

    print("Dataset generated:", df.shape)
    print("\nSamples per disease:\n", df["Disease"].value_counts())

    return df


# -----------------------------
# TRAIN MODEL (OPTIMIZED)
# -----------------------------
def train_model(df):
    X = df.drop("Disease", axis=1)
    y = df["Disease"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # ✅ Optimized model (NO crash)
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=1
    )

    model = CalibratedClassifierCV(
        rf,
        method='sigmoid',
        cv=3
    )

    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nModel Accuracy: {round(accuracy*100, 2)}%")

    return model, X.columns


# -----------------------------
# SAVE MODEL SAFELY
# -----------------------------
def save_model(model, features):
    temp_model = "model_temp.pkl"
    temp_feat = "features_temp.pkl"

    with open(temp_model, "wb") as f:
        pickle.dump(model, f)

    with open(temp_feat, "wb") as f:
        pickle.dump(list(features), f)

    os.replace(temp_model, "model.pkl")
    os.replace(temp_feat, "features.pkl")

    print("Model and features saved successfully.")


# -----------------------------
# MAIN PIPELINE
# -----------------------------
if __name__ == "__main__":
    df = generate_dataset(samples_per_disease=800)  # ~12,000 rows
    model, features = train_model(df)
    save_model(model, features)