import serial
import time

ser = None

# -------------------------------
# DISEASE → COMMAND MAP (15)
# -------------------------------
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
    "Skin Infection": "MED12",

    # 👻 PHANTOM (NO REAL MOTOR)
    "Typhoid": "MED13",
    "Dengue": "MED14",
    "Pneumonia": "MED15"
}

# -------------------------------
# INIT SERIAL (KEEP SAME STYLE)
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

    # Initialize serial if needed
    if ser is None:
        init_serial()

    # -------------------------------
    # SEND COMMAND (AUGER SYSTEM)
    # -------------------------------
    if ser:
        try:
            ser.write((command + "\n").encode())
            print(f"Sent: {command}")

            # Optional: read response from ESP32
            time.sleep(0.2)
            while ser.in_waiting:
                response = ser.readline().decode().strip()
                print(f"ESP: {response}")

        except Exception as e:
            print(f"Serial write failed: {e}")
    else:
        print(f"[SIMULATION] {command}")