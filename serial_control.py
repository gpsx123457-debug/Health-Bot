import serial
import time

SERIAL_PORT = "COM6"   # 🔴 CHANGE if needed
BAUD_RATE = 115200

ser = None

# -------------------------------
# CONNECT FUNCTION
# -------------------------------
def connect():
    global ser
    if ser is None:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # allow ESP reset

# -------------------------------
# SEND COMMAND
# -------------------------------
def send_command(cmd):
    try:
        connect()  # ✅ now defined
        print(">>> Sending:", cmd)   # debug
        ser.write((cmd + "\n").encode())
        return f"Sent: {cmd}"
    except Exception as e:
        return str(e)