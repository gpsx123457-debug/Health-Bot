import serial
import time

ser = None

disease_to_command = {
    "Flu": "MED1",
    "Viral Infection": "MED2",
    "Common Cold": "MED3",
    "Allergy": "MED4",
    "Gastritis": "MED5",
    "Food Poisoning": "MED6",
    "Migraine": "MED7",
    "Asthma": "MED8",
    "Cuts Bruises": "MED9",
    "Burns Mild": "MED10",
    "Burns Severe": "MED11",
    "Skin Infection": "MED12"
}

# -------------------------------
# INIT SERIAL ONLY WHEN CALLED
# -------------------------------
def init_serial(port='COM6', baud=115200):
    global ser
    if ser is None:
        try:
            ser = serial.Serial(port, baud, timeout=1)
            time.sleep(2)
            print("Serial connected")
        except Exception as e:
            print(f"Serial init failed: {e}")
            ser = None

# -------------------------------
# DISPENSE FUNCTION
# -------------------------------
def dispense_medicine(disease_name):
    global ser

    if disease_name not in disease_to_command:
        print("No mapping for disease")
        return

    command = disease_to_command[disease_name]

    if ser is None:
        init_serial()

    if ser:
        try:
            ser.write((command + "\n").encode())
            print(f"Sent: {command}")
        except Exception as e:
            print(f"Serial write failed: {e}")
    else:
        print(f"[SIMULATION] {command}")