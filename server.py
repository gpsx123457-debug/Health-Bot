from fastapi import FastAPI
import serial
import time

app = FastAPI()

# -------------------------------
# CONFIG (CHANGE THIS)
# -------------------------------
SERIAL_PORT = "COM6"   # change if needed
BAUD_RATE = 115200

ser = None

# -------------------------------
# INIT SERIAL
# -------------------------------
def init_serial():
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print("✅ Serial connected")
    except Exception as e:
        print(f"❌ Serial error: {e}")
        ser = None

init_serial()

# -------------------------------
# ROOT CHECK
# -------------------------------
@app.get("/")
def home():
    return {"status": "Server running"}

# -------------------------------
# DISPENSE ENDPOINT
# -------------------------------
@app.post("/dispense/{med}")
def dispense(med: str):
    global ser

    med = med.upper()

    if med not in ["MED1", "MED2", "MED3", "MED4"]:
        return {"error": "Invalid command"}

    if ser is None:
        return {"error": "Serial not connected"}

    try:
        ser.write((med + "\n").encode())
        print(f"➡ Sent: {med}")

        return {"status": f"{med} sent"}

    except Exception as e:
        return {"error": str(e)}