import requests

# -------------------------------
# ESP32 DIRECT IP
# -------------------------------
SERVER_URL = "http://10.120.25.76"

# -------------------------------
# DISEASE → MOTOR MAP
# -------------------------------
disease_to_command = {
    "Flu": "MED1",
    "Viral Infection": "MED1",
    "Common Cold": "MED1",

    "Allergy": "MED2",
    "Gastritis": "MED2",
    "Food Poisoning": "MED2",

    "Migraine": "MED3",
    "Asthma": "MED3",
    "Skin Infection": "MED3",

    "Cuts Bruises": "MED4",
    "Burns Mild": "MED4",
    "Burns Severe": "MED4",

    "Typhoid": None,
    "Dengue": None,
    "Pneumonia": None
}

# -------------------------------
# DISPENSE FUNCTION
# -------------------------------
def dispense_medicine(disease_name):
    command = disease_to_command.get(disease_name)

    if not command:
        print("No hardware action required")
        return

    url = f"{SERVER_URL}/dispense/{command}"

    try:
        print("➡ Sending:", url)

        response = requests.get(url, timeout=5)

        print("Status:", response.status_code)
        print("Response:", response.text)

    except Exception as e:
        print("❌ ERROR:", e)