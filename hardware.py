import requests

# -------------------------------
# NGROK SERVER URL (FIXED)
# -------------------------------
SERVER_URL = " https://madelynn-polyprotic-feasibly.ngrok-free.dev"

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
    command = disease_to_command.get(disease_name)

    if not command:
        print("No mapping / No hardware action")
        return

    try:
        url = f"{SERVER_URL}/{command}"   # FINAL CORRECT URL
        response = requests.post(url)

        print(f"Sent to server: {url}")
        print(f"Response: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Request failed: {e}")