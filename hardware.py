import serial
import time

ser = serial.Serial('COM6', 115200, timeout=1)
time.sleep(2)

# Disease → MED command mapping (12 servos)
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

def dispense_medicine(disease_name):
    if disease_name in disease_to_command:
        command = disease_to_command[disease_name]
        ser.write((command + '\n').encode())
        print(f"Sent: {command}")
    else:
        print("Disease not mapped to servo")