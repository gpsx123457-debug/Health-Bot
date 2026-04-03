from serial_control import send_command
import time

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
# DISPENSE FUNCTION (SERIAL)
# -------------------------------
def dispense_medicine(disease_name, spins=1):
    command = disease_to_command.get(disease_name)

    if not command:
        print("No hardware action required")
        return

    try:
        for _ in range(spins):
            print(f"➡ Sending: {command}")
            response = send_command(command)
            print(response)
            time.sleep(1.2)

    except Exception as e:
        print("❌ ERROR:", e)