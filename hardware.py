import requests

# -------------------------------
# NGROK SERVER URL
# -------------------------------
SERVER_URL = "https://192.168.29.230:8000"

# -------------------------------
# DISEASE → MOTOR MAP
# -------------------------------
disease_to_command = {
    "Flu": "MED1",
    "Viral Infection": "MED2",
    "Common Cold": "MED3",
    "Allergy": "MED4",

    "Gastritis": "MED1",
    "Food Poisoning": "MED2",
    "Migraine": "MED3",
    "Asthma": "MED4",
    "Cuts Bruises": "MED1",
    "Burns Mild": "MED2",
    "Burns Severe": "MED3",
    "Skin Infection": "MED4",

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

    try:
        url = f"{SERVER_URL}/dispense/{command}"

        print("Sending request:", url)

        response = requests.post(url)

        print("Status:", response.status_code)
        print("Response:", response.text)

    except Exception as e:
        print("Request failed:", e)