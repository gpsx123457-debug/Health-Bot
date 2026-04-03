import serial
import time
import threading

SERIAL_PORT = "COM6"
BAUD_RATE = 115200

ser = None
lock = threading.Lock()

last_cmd = None
last_time = 0
DEBOUNCE_SEC = 1.0


def connect():
    global ser
    if ser is None:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # ESP reset delay


def send_command(cmd: str):
    """
    Low-level serial send with debounce + thread safety
    """
    global last_cmd, last_time

    with lock:
        now = time.time()

        # prevent duplicate spam from Streamlit reruns
        if cmd == last_cmd and (now - last_time) < DEBOUNCE_SEC:
            return f"Ignored duplicate: {cmd}"

        connect()

        try:
            ser.reset_input_buffer()

            ser.write((cmd.strip() + "\n").encode())

            last_cmd = cmd
            last_time = now

            return f"Sent: {cmd}"

        except Exception as e:
            return f"Serial error: {e}"


def dispatch(cmd: str, spins: int = 1):
    """
    High-level safe entry point used by app.py
    """
    results = []

    for _ in range(spins):
        res = send_command(cmd)
        print("[DISPATCH]", res)
        results.append(res)
        time.sleep(1.2)  # motor cooldown window

    return results