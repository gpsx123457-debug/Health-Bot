from fastapi import FastAPI
import requests

app = FastAPI()

ESP32_IP = "http://10.120.25.76"  # your ESP IP

@app.get("/med/{id}")
def dispense(id: str):
    try:
        url = f"{ESP32_IP}/MED{id}"
        r = requests.get(url, timeout=5)
        return {"esp32_response": r.text}
    except Exception as e:
        return {"error": str(e)}