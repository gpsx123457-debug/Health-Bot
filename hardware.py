import requests

# -------------------------------
# CHANGE THIS → YOUR NGROK URL
# -------------------------------
SERVER_URL = "https://your-ngrok-url/dispense"

# -------------------------------
# DISEASE → MOTOR MAP (4 REAL + PHANTOM)
# -------------------------------
disease_to_command = {
    # REAL MOTORS
    "Flu": "MED1",
    "Viral Infection": "MED2",
    "Common Cold": "MED3",
    "Allergy": "MED4",

    # 👻 PHANTOM (mapped but NOT physically present)
    "Gastritis": "MED1",
    "Food Poisoning": "MED2",
    "Migraine": "MED3",
    "Asthma": "MED4",
    "Cuts Bruises": "MED1",
    "Burns Mild": "MED2",
    "Burns Severe": "MED3",
    "Skin Infection": "MED4",

    # NO DISPENSE
    "Typhoid": None,
    "Dengue": None,
    "Pneumonia": None
}

# -------------------------------
# DISPENSE FUNCTION (API BASED)
# -------------------------------
def dispense_medicine(disease_name):

    if disease_name not in disease_to_command:
        print("No mapping")
        return

    command = disease_to_command[disease_name]

    if command is None:
        print("No hardware action required")
        return

    try:
        response = requests.post(f"{SERVER_URL}/{command}")

        if response.status_code == 200:
            print(f"✅ Sent: {command}")
        else:
            print("❌ Server error")

    except Exception as e:
        print(f"❌ Request failed: {e}")