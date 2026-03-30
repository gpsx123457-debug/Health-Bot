import pandas as pd
import random
import joblib

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
# DISEASE DEFINITIONS
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
# DATASET GENERATION
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

            duration = random.randint(0, 2)
            age = random.randint(0, 2)
            condition = random.randint(0, 2)

            row += [duration, age, condition, disease]
            rows.append(row)

    df = pd.DataFrame(rows, columns=columns)
    df = df.sample(frac=1).reset_index(drop=True)

    return df


# -----------------------------
# TRAIN MODEL
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

    rf = RandomForestClassifier(
        n_estimators=150,
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

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nAccuracy: {round(accuracy * 100, 2)}%")

    return model, X.columns


# -----------------------------
# SAVE MODEL
# -----------------------------
def save_model(model, features):
    joblib.dump(model, "model.pkl", compress=3)
    joblib.dump(list(features), "features.pkl")

    print("✅ model.pkl and features.pkl saved")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    df = generate_dataset()
    model, features = train_model(df)
    save_model(model, features)