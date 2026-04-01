import streamlit as st
from model import predict
from database import init_db, insert_record
import datetime
import time

# ===============================
# HARDWARE IMPORT SAFE MODE
# ===============================
try:
    from hardware import dispense_medicine
    HARDWARE_AVAILABLE = True
except:
    HARDWARE_AVAILABLE = False

HARDWARE_ENABLED = HARDWARE_AVAILABLE

# ===============================
# SERIAL (DIRECT ESP CONTROL FIX)
# ===============================
try:
    import serial

    @st.cache_resource
    def init_serial():
        try:
            esp = serial.Serial("COM5", 115200, timeout=1)
            time.sleep(2)
            return esp
        except:
            return None

    esp = init_serial()
    SERIAL_AVAILABLE = esp is not None

except:
    esp = None
    SERIAL_AVAILABLE = False

init_db()

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="Health AI", layout="wide")

# ===============================
# SESSION STATE
# ===============================
if "page" not in st.session_state:
    st.session_state.page = 0
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "data" not in st.session_state:
    st.session_state.data = {}
if "billing" not in st.session_state:
    st.session_state.billing = {}
if "dispensed" not in st.session_state:
    st.session_state.dispensed = False
if "busy" not in st.session_state:
    st.session_state.busy = False
if "last_cmd" not in st.session_state:
    st.session_state.last_cmd = None

# ===============================
# NAVIGATION
# ===============================
def next_page():
    st.session_state.page += 1

def restart():
    st.session_state.page = 0
    st.session_state.data = {}
    st.session_state.billing = {}
    st.session_state.dispensed = False
    st.session_state.busy = False

# ===============================
# TRANSLATION SYSTEM (FULL RESTORED)
# ===============================
TEXT = {
    "English": {
        "language": "Language",
        "select": "Select",
        "next": "Next ➡️",
        "details": "User Details",
        "name": "Name",
        "age": "Age",
        "dob": "Date of Birth",
        "symptoms": "Select Symptoms",
        "severity": "Severity",
        "duration": "Duration (days)",
        "result": "Diagnosis Result",
        "confidence": "Confidence",
        "medicine": "Medicine",
        "dose": "Dose",
        "timing": "Timing",
        "type": "Type",
        "days": "Days (1-5)",
        "total": "Total Cost",
        "proceed": "Proceed ➡️",
        "pay_done": "Payment Done",
        "success": "Medicine Dispensed Successfully",
        "thanks": "Thank you for using the service",
        "restart": "Restart"
    },
    "Hindi": {
        "language": "भाषा",
        "select": "चुनें",
        "next": "आगे ➡️",
        "details": "उपयोगकर्ता विवरण",
        "name": "नाम",
        "age": "आयु",
        "dob": "जन्म तिथि",
        "symptoms": "लक्षण चुनें",
        "severity": "गंभीरता",
        "duration": "अवधि (दिन)",
        "result": "निदान परिणाम",
        "confidence": "विश्वास",
        "medicine": "दवा",
        "dose": "खुराक",
        "timing": "समय",
        "type": "प्रकार",
        "days": "दिन (1-5)",
        "total": "कुल लागत",
        "proceed": "आगे ➡️",
        "pay_done": "भुगतान पूर्ण",
        "success": "दवा सफलतापूर्वक दी गई",
        "thanks": "सेवा उपयोग करने के लिए धन्यवाद",
        "restart": "पुनः प्रारंभ"
    }
}

T = TEXT[st.session_state.lang]

# ===============================
# SAFE MOTOR FUNCTION
# ===============================
def send_motor(cmd):

    if st.session_state.busy:
        st.warning("Motor busy...")
        return

    st.session_state.busy = True

    try:
        if SERIAL_AVAILABLE:
            esp.write((cmd + "\n").encode())
            esp.flush()
            time.sleep(1.5)
            st.success(f"Sent: {cmd}")

        elif HARDWARE_ENABLED:
            dispense_medicine(cmd)
            st.success(f"Hardware call: {cmd}")

        else:
            st.warning(f"Simulation: {cmd}")

        st.session_state.last_cmd = cmd

    except Exception as e:
        st.error(f"Error: {e}")

    st.session_state.busy = False

# ===============================
# SYMPTOMS
# ===============================
symptoms = [
    "Fever","Cough","Headache","Fatigue","Nausea","Vomiting",
    "Diarrhea","BodyPain","SoreThroat","RunnyNose"
]

SYMPTOMS_T = {
    "English": {s: s for s in symptoms},
    "Hindi": {
        "Fever":"बुखार","Cough":"खांसी","Headache":"सिरदर्द","Fatigue":"थकान",
        "Nausea":"मतली","Vomiting":"उल्टी","Diarrhea":"दस्त",
        "BodyPain":"शरीर दर्द","SoreThroat":"गले में दर्द","RunnyNose":"नाक बहना"
    }
}

# ===============================
# MEDICATION DATABASE
# ===============================
medications = {
    "Flu": {"name":"Paracetamol","dose":"500mg","freq":3,"timing":"After food","type":"tablet","price":5},
    "Common Cold": {"name":"Cetirizine","dose":"10mg","freq":1,"timing":"Night","type":"tablet","price":8},
    "Allergy": {"name":"Cetirizine","dose":"10mg","freq":1,"timing":"Night","type":"tablet","price":8},
    "Migraine": {"name":"Ibuprofen","dose":"400mg","freq":2,"timing":"After food","type":"tablet","price":7},
    "Viral Infection": {"name":"Paracetamol","dose":"500mg","freq":3,"timing":"After food","type":"tablet","price":5}
}

# ===============================
# PAGE 0 - LANGUAGE
# ===============================
if st.session_state.page == 0:

    st.title(T["language"])

    lang = st.selectbox("Select Language", ["English","Hindi"])

    if st.button("Next"):
        st.session_state.lang = lang
        st.session_state.page = 1

# ===============================
# PAGE 1 - USER DETAILS
# ===============================
elif st.session_state.page == 1:

    st.title(T["details"])

    st.session_state.data["name"] = st.text_input(T["name"])

    today = datetime.date.today()
    dob = st.date_input(T["dob"])

    age = today.year - dob.year
    st.session_state.data["age"] = age

    st.write(f"{T['age']}: {age}")

    if st.button(T["next"]):
        st.session_state.page = 2

# ===============================
# PAGE 2 - SYMPTOMS
# ===============================
elif st.session_state.page == 2:

    st.title(T["symptoms"])

    data = {}
    for s in symptoms:
        data[s] = st.checkbox(SYMPTOMS_T[st.session_state.lang][s])

    st.session_state.data["symptoms"] = data

    if st.button(T["next"]):
        st.session_state.page = 3

# ===============================
# PAGE 3 - SEVERITY
# ===============================
elif st.session_state.page == 3:

    severity = st.selectbox(T["severity"], ["Low","Moderate","High"])
    duration = st.number_input(T["duration"], 1, 30, 1)

    st.session_state.data.update({
        "Condition": ["Low","Moderate","High"].index(severity),
        "Duration": duration
    })

    if st.button(T["next"]):
        st.session_state.page = 4

# ===============================
# PAGE 4 - PREDICTION
# ===============================
elif st.session_state.page == 4:

    user_input = {}
    user_input.update(st.session_state.data["symptoms"])
    user_input.update({
        "Duration": st.session_state.data["Duration"],
        "Condition": st.session_state.data["Condition"]
    })

    result = predict(user_input)
    st.session_state.result = result

    st.success(result["prediction"])
    st.progress(result["confidence"]/100)

    if st.button(T["next"]):
        st.session_state.page = 5

# ===============================
# PAGE 5 - MEDICINE
# ===============================
elif st.session_state.page == 5:

    disease = st.session_state.result["prediction"]
    med = medications.get(disease, medications["Viral Infection"])

    st.write(med["name"])
    st.write(med["dose"])
    st.write(med["timing"])
    st.write(med["type"])

    days = st.number_input(T["days"], 1, 5, 1)

    units = med["freq"] * days
    cost = units * med["price"]

    st.session_state.billing = {"units": units, "cost": cost}

    st.write(f"{T['total']}: ₹{cost}")

    if st.button(T["proceed"]):
        st.session_state.page = 6

# ===============================
# PAGE 6 - PAYMENT + DISPENSE
# ===============================
elif st.session_state.page == 6:

    bill = st.session_state.billing

    st.write(f"{T['amount']}: ₹{bill['cost']}")
    st.code(f"upi://pay?pa=healthai@upi&am={bill['cost']}")

    if st.button(T["pay_done"]):

        if not st.session_state.dispensed:

            disease = st.session_state.result["prediction"]

            send_motor(disease)

            insert_record({
                "name": st.session_state.data.get("name",""),
                "age": st.session_state.data.get("age",0),
                "disease": disease,
                "cost": bill["cost"]
            })

            st.session_state.dispensed = True
            st.session_state.page = 7

# ===============================
# PAGE 7 - SUCCESS
# ===============================
elif st.session_state.page == 7:

    st.success(T["success"])
    st.write(T["thanks"])

    if st.button(T["restart"]):
        restart()